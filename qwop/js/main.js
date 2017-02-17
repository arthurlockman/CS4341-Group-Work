// Please don't touch. Needed for Box2d. Mystery constants.
var autoReset = true
var requestReset = true
var requestTeleport = true

// GLOBALS
var ITERATIONS_PER_SECOND = 600
var FRAMERATE = 60

// World properties
var worldWidth = worldHeight = 500
var canvasWidth = canvasHeight= 1054

/* PROGRAM STARTS HERE */
main()

function main() {

    var inputManager = new InputManager(document)

    var g = new Genome(600, 0.1)

    var p1 = new Promise((resolve, reject) => 
        evaluate(resolve, reject, g)
    )

    // var p2 = new Promise((resolve, reject) => 
    //     evaluate(resolve, reject, inputManager)
    // )

    // Promise.all([p1, p2]).then((val) => console.log(val))
    Promise.all([p1]).then((val) => console.log(val))

}

function evaluate(resolve, reject, inputManager) {

    // Init objects
    var character = new Character()
    var world = new World(worldWidth, worldHeight, character)
    var game = new Game(world, character)
    var display = new Display(document, canvasWidth, canvasHeight, world, worldWidth, worldHeight)

    // This starts the runner
    game.resetRunner()

        // This runs the display loop
    var displayIntervalId = setInterval(
        function() {
            display.clearCurrentFrame()
            display.drawWorld()
            display.displayStats(game.farthestDistTraveled, game.elapsedTime, game.totalDistTraveled)
        },
        1000 / FRAMERATE)

    var score;

    // This runs the main loop
    var gameIntervalId = setInterval(
        function() {
           output = game.run(world, character, inputManager)

            if(output.has_fallen == true) {
                score = output.score
                clearInterval(displayIntervalId)
                clearInterval(gameIntervalId)
                console.log(score)
                resolve(score)
            }
        },
        1000 / ITERATIONS_PER_SECOND)
}