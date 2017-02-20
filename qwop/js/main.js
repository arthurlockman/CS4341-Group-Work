// Please don't touch. Needed for Box2d. Mystery constants.
var autoReset = true;
var requestReset = true;
var requestTeleport = true;

// GLOBALS
var ITERATIONS_PER_SECOND = 600;
var FRAMERATE = 60;
var DISPLAY = true;

// World properties
var worldWidth = worldHeight = 500;
var canvasWidth = canvasHeight= 1054;

/* PROGRAM STARTS HERE */
main();

function main() {

    // This is for controlling the guy manually
    // var inputManager = new InputManager(document)
    // promises = [new Promise((resolve, reject) => evaluate(resolve, reject, inputManager))]
    
    // This is for GA
    // var ga = new GeneticAlgorithm(600, 30, 0.1, 0.1, 10, evaluate)

    //NN Example
    var nn = new NeuralNet();
    promises.push(
        new Promise((resolve, reject) =>
            evaluateNN(resolve, reject, nn, 10000)
    ));

    Promise.all(promises).then((val) => {
        console.log(val);
    });

}

function evaluate(resolve, reject, inputManager) {

    // Init objects
    var character = new Character();
    var world = new World(worldWidth, worldHeight, character);
    var game = new Game(world, character);
    inputManager.setWorldVariables(character, world);

    var display;
    if(DISPLAY) {
        display = new Display(document, canvasWidth, canvasHeight, world, worldWidth, worldHeight)    
    }

    // This starts the runner
    game.resetRunner();

    // This runs the display loop
    if(DISPLAY) {
        var displayIntervalId = setInterval(
            function() {
                display.clearCurrentFrame();
                display.drawWorld();
                display.displayStats(game.farthestDistTraveled, game.elapsedTime, game.totalDistTraveled)
            },
            1000 / FRAMERATE)
    }

    // This runs the main loop
    var gameIntervalId = setInterval(
        function() {
            output = game.run(world, character, inputManager);

            if(output.has_fallen == true || game.elapsedTime > 9.9) {
                score = output.score;
                clearInterval(gameIntervalId);
                if(DISPLAY) { clearInterval(displayIntervalId) }
                inputManager.learn(-10);
                resolve(score);
            } else {
                inputManager.learn(output.score);
            }
        },
        1000 / ITERATIONS_PER_SECOND)
}

function evaluateNN(resolve, reject, inputManager, iterations, counter=0) {
    // Init objects
    var character = new Character();
    var world = new World(worldWidth, worldHeight, character);
    var game = new Game(world, character);
    inputManager.setWorldVariables(character, world);

    var display;
    if(DISPLAY) {
        display = new Display(document, canvasWidth, canvasHeight, world, worldWidth, worldHeight)
    }

    // This starts the runner
    game.resetRunner();

    // This runs the display loop
    if(DISPLAY) {
        var displayIntervalId = setInterval(
            function() {
                display.clearCurrentFrame();
                display.drawWorld();
                display.displayStats(game.farthestDistTraveled, game.elapsedTime, game.totalDistTraveled)
            },
            1000 / FRAMERATE)
    }

    // This runs the main loop
    var gameIntervalId = setInterval(
        function() {
            output = game.run(world, character, inputManager);

            if(output.has_fallen == true || game.elapsedTime > 9.9) {
                score = output.score;
                clearInterval(gameIntervalId);
                if(DISPLAY) { clearInterval(displayIntervalId) }
                if (counter == iterations) {
                    resolve(score)
                } else {
                    console.log('Iteration ' + counter + ': ' + score);
                    evaluateNN(resolve, reject, inputManager, iterations, counter + 1);
                }
            } else {
                inputManager.learn(output.score);
            }
        },
        1000 / ITERATIONS_PER_SECOND)
}