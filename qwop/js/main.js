// Please don't touch. Needed for Box2d. Mystery constants.
var autoReset = true
var requestReset = true
var requestTeleport = true

// GLOBALS
var ITERATIONS_PER_SECOND = 60
var FRAMERATE = 60

/* PROGRAM STARTS HERE */
main()

function main() {

    // World properties
    var worldWidth = worldHeight = 500
    var canvasWidth = canvasHeight= 1054

    // Init objects
    var character = new Character()
    var world = new World(worldWidth, worldHeight, character)
    var game = new Game(world, character)
    var inputManager = new InputManager(document, character, game)
    var display = new Display(document, canvasWidth, canvasHeight, world, worldWidth, worldHeight)

    // This starts the runner
    game.resetRunner()

    // This runs the main loop
    setInterval(
        function() {
            game.run(world, character, inputManager, game)
        },
        1000 / ITERATIONS_PER_SECOND)

    // This runs the display loop
    setInterval(
        function() {
            display.clearCurrentFrame()
            display.drawWorld()
            display.displayStats(game.farthestDistTraveled, game.elapsedTime, game.totalDistTraveled)
        },
        1000 / FRAMERATE)
}