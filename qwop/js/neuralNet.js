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

    train() {
        setInterval(function(){ // start the learning loop
            var action = this.agent.act(s); // s is an array of length 8
            //... execute action in environment and get the reward
            this.agent.learn(reward); // the agent improves its Q,policy,model, etc. reward is a float
        }, 0);
    }
}
