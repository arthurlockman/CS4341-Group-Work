class NeuralNet {
    constructor() {
        // create an environment object
        this.env = {};
        this.env.getNumStates = function() { return 10; };
        // 11 actions: Nothing (N) Q W O P QW OP QO QP WO WP
        this.env.getMaxNumActions = function() { return 11; };

        // create the DQN agent
        this.spec = {};
        this.spec.update = 'qlearn'; // qlearn | sarsa
        // https://studywolf.wordpress.com/2013/07/01/reinforcement-learning-sarsa-vs-q-learning/
        this.spec.gamma = 0.9; // discount factor, [0, 1)
        this.spec.epsilon = 0.2; // initial epsilon for epsilon-greedy policy, [0, 1)
        this.spec.alpha = 0.01; // value function learning rate
        this.spec.experience_add_every = 10; // number of time steps before we add another experience to replay memory
        this.spec.experience_size = 5000; // size of experience replay memory
        this.spec.learning_steps_per_iteration = 20;
        this.spec.tderror_clamp = 1.0; // for robustness
        this.spec.num_hidden_units = 8; // number of neurons in hidden layer
        this.actions = ['Q', 'W', 'O', 'P', 'QW', 'QO', 'QP', 'WO', 'WP', 'OP', 'N'];
        this.agent = new RL.DQNAgent(this.env, this.spec);
        this.lastScore = 0;
    }

    learn(score) {
        // console.log((score - this.lastScore) * 10.0);
        this.agent.learn((score - this.lastScore) * 10.0);
        this.lastScore = score;
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
        var action = this.agent.act(this.getState());
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
}
