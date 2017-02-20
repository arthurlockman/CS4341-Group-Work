class NeuralNet {
    constructor() {
        // https://cs.stanford.edu/people/karpathy/convnetjs/demo/rldemo.html
        var num_inputs = 11;
        var num_actions = 10; // 5 possible angles agent can turn
        var temporal_window = 1; // amount of temporal memory. 0 = agent lives in-the-moment :)
        var network_size = num_inputs*temporal_window + num_actions*temporal_window + num_inputs;
        var layer_defs = [];
        layer_defs.push({type:'input', out_sx:1, out_sy:1, out_depth:network_size});
        layer_defs.push({type:'fc', num_neurons: 6, activation:'relu'});
        layer_defs.push({type:'fc', num_neurons: 6, activation:'relu'});
        layer_defs.push({type:'regression', num_neurons:num_actions});
        var tdtrainer_options = {learning_rate:0.001, momentum:0.0, batch_size:64, l2_decay:0.01};
        var opt = {};
        opt.temporal_window = temporal_window;
        opt.experience_size = 30000;
        opt.start_learn_threshold = 1000;
        opt.gamma = 0.7;
        opt.learning_steps_total = 200000;
        opt.learning_steps_burnin = 3000;
        opt.epsilon_min = 0.05;
        opt.epsilon_test_time = 0.05;
        opt.layer_defs = layer_defs;
        opt.tdtrainer_options = tdtrainer_options;
        this.brain = new deepqlearn.Brain(num_inputs, num_actions, opt); // woohoo
        this.lastScore = 0;
        this.actions = ['Q', 'W', 'O', 'P', 'QW', 'QO', 'QP', 'WO', 'WP', 'OP', 'N'];
    }

    learn(score) {
        // console.log((score - this.lastScore) * 10.0);
        var _score = (score - this.lastScore) * 10.0;
        this.brain.backward(_score);
        this.lastScore = score;
        return _score;
    }

    setWorldVariables(character, world) {
        /** @type {(Character)} */
        this.character = character;
        /** @type {(World)} */
        this.world = world;
        this.lastScore = 0;
    }

    getState() {
        var state = [];
        state[state.length] = this.character.curVelX;
        state[state.length] = this.character.curX;
        state[state.length] = this.character.joint.r_hip.GetJointAngle();
        state[state.length] = this.character.joint.l_hip.GetJointAngle();
        state[state.length] = this.character.joint.r_knee.GetJointAngle();
        state[state.length] = this.character.joint.l_knee.GetJointAngle();
        state[state.length] = this.character.getLeftFootX(this.character.body);
        state[state.length] = this.character.getLeftFootY(this.character.body);
        state[state.length] = this.character.getRightFootX(this.character.body);
        state[state.length] = this.character.getRightFootY(this.character.body);
        return state;
    }

    /**
     * Get input for a character state.
     * @returns {[number,number,number,number]} [Q, W, O, P] 1 if pressed, 0 otherwise
     */
    getInput() {
        var action = this.brain.forward(this.getState());
        var _a = this.actions[action];
        var move = [0, 0, 0, 0];
        if (_a.includes('Q'))
            move[0] = 1;
        if (_a.includes('W'))
            move[1] = 1;
        if (_a.includes('O'))
            move[2] = 1;
        if (_a.includes('P'))
            move[3] = 1;
        return move;
    }

    /**
     * Convert net to JSON string representation.
     */
    toJSON() {
        var j = this.brain.value_net.toJSON();
        var t = JSON.stringify(j);
        return t;
    }
}
