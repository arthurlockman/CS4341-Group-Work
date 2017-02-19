class NeuralNet {
    constructor() {
        // create an environment object
        this.env = {};
        this.env.getNumStates = function() { return 8; };
        // 11 actions: Nothing (N) Q W O P QW OP QO QP WO WP
        this.env.getMaxNumActions = function() { return 10; };

        // create the DQN agent
        this.spec = { alpha: 0.01 }; // see full options on DQN page
        this.actions = ['Q', 'W', 'O', 'P', 'QW', 'QO', 'QP', 'WO', 'WP', 'OP', 'N'];
        this.agent = new RL.DQNAgent(this.env, this.spec);
    }

    run() {

    }

    /**
     * Get input for a character state.
     * @param state The state.
     * @returns {[number,number,number,number]} [Q, W, O, P] 1 if pressed, 0 otherwise
     */
    getInput(state) {
        // TODO: Need to get input and put in S (array of state variables)
        var action = this.agent.act(state);
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
        // TODO: Get reward
        this.agent.learn(reward);
        return move;
    }
}
