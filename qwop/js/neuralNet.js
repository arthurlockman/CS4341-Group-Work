class NeuralNet {
    constructor() {
        // create an environment object
        this.env = {};
        this.env.getNumStates = function() { return 6; };
        // 11 actions: Nothing (N) Q W O P QW OP QO QP WO WP
        this.env.getMaxNumActions = function() { return 11; };

        // create the DQN agent
        this.spec = { alpha: 0.1, num_hidden_units: 2 }; // see full options on DQN page
        this.actions = ['Q', 'W', 'O', 'P', 'QW', 'QO', 'QP', 'WO', 'WP', 'OP', 'N'];
        this.agent = new RL.DQNAgent(this.env, this.spec);
        this.lastScore = 0;
    }

    learn(score) {
        this.agent.learn((score - this.lastScore) * 10.0);
        this.lastScore = score;
    }

    setWorldVariables(character, world) {
        /** @type {(Character)} */
        this.character = character;
        /** @type {(World)} */
        this.world = world;
    }

    getState() {
        var state = [];
        state[state.length] = this.character.curVelX;
        state[state.length] = this.character.curX;
        state[state.length] = this.character.joint.r_hip.GetJointAngle();
        state[state.length] = this.character.joint.l_hip.GetJointAngle();
        state[state.length] = this.character.joint.r_knee.GetJointAngle();
        state[state.length] = this.character.joint.l_knee.GetJointAngle();
        return state;
    }

    /**
     * Get input for a character state.
     * @returns {[number,number,number,number]} [Q, W, O, P] 1 if pressed, 0 otherwise
     */
    getInput() {
        // TODO: Need to get input and put in S (array of state variables)
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
