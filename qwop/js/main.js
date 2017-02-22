// Please don't touch. Needed for Box2d. Mystery constants.
var autoReset = true;
var requestReset = true;
var requestTeleport = true;

// GLOBALS
var ITERATIONS_PER_SECOND = 600;
var FRAMERATE = 60;
var DISPLAY = true;
var NN_RUNTIME = 30.0;
var REWARD_AFTER_EACH_SIM = false;

// World properties
var worldWidth = worldHeight = 500;
var canvasWidth = canvasHeight= 1054;
var reward_graph;

// Query string getter
var QueryString = function () {
  // This function is anonymous, is executed immediately and 
  // the return value is assigned to QueryString!
  var query_string = {};
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
        // If first entry with this name
    if (typeof query_string[pair[0]] === "undefined") {
      query_string[pair[0]] = decodeURIComponent(pair[1]);
        // If second entry with this name
    } else if (typeof query_string[pair[0]] === "string") {
      var arr = [ query_string[pair[0]],decodeURIComponent(pair[1]) ];
      query_string[pair[0]] = arr;
        // If third or later entry with this name
    } else {
      query_string[pair[0]].push(decodeURIComponent(pair[1]));
    }
  } 
  return query_string;
}();

document.getElementById("run").addEventListener("click", function() {
    window.location.href = "/index.html?alg=" + document.getElementById("algorithmSelector").value
});

/* PROGRAM STARTS HERE */
main();

function main() 
{
    reward_graph = new cnnvis.Graph();
    var select = document.getElementById("algorithmSelector");
    if (QueryString.alg) {
        select.value = QueryString.alg
    }
    if (QueryString.nnreward) {
        if (QueryString.nnreward == "eachsim") {
            REWARD_AFTER_EACH_SIM = true;
            document.getElementById("rewardtype").innerHTML = "<p>Rewarding after each simulation</p>"
        }
    }
    if (select.value == "nn")
    {
        //NN Example
        var promises = [];
        var nn = new NeuralNet();
        document.getElementById("dump").addEventListener("click", function() {
            document.getElementById("networkDumpTextBox").value = nn.toJSON();
        });
        document.getElementById("load").addEventListener("click", function() {
            nn.fromJSON(document.getElementById("networkLoadTextBox").value);
        });
        document.getElementById("dump").style.display = 'block';
        document.getElementById("networkDumpTextBox").style.display = 'block';
        document.getElementById("load").style.display = 'block';
        document.getElementById("networkLoadTextBox").style.display = 'block';
        promises.push(
            new Promise((resolve, reject) =>
                evaluateNN(resolve, reject, nn, 100000)
        ));
        resetOutput();
        printOutput("Iteration, Score, Time, Average Reward");
    
        Promise.all(promises).then((val) => {
            console.log(val);
        });
    } else if (select.value == "ga") 
    {
        resetOutput();
        printOutput("Generation, Score, Time");
        var ga = new GeneticAlgorithm(NN_RUNTIME * 60, 30, 0.1, 0.1, 10, evaluateGA);
    } else if (select.value == "manual")
    {
        var inputManager = new InputManager(document);
        promises = [new Promise((resolve, reject) => evaluateManual(resolve, reject, inputManager))];
        Promise.all(promises).then((val) => {
            console.log(val);
        });
    }
}

function drawGraph(x, y) {
    reward_graph.add(x, y);
    var gcanvas = document.getElementById("graph_canvas");
    reward_graph.drawSelf(gcanvas);
}

function printOutput(output) {
    var box = document.getElementById("outputTextBox");
    box.value += output + '\n';
}

function resetOutput() {
    var box = document.getElementById("outputTextBox");
    box.value = ""
}

function evaluateGA(resolve, reject, inputManager) {

    // Init objects
    var character = new Character();
    var world = new World(worldWidth, worldHeight, character);
    var game = new Game(world, character);
    inputManager.setWorldVariables(character, world);
    inputManager.game = game;

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
                printOutput(1 + ', ' + score + ', ' + game.elapsedTime);
                resolve(score);
            } else {
                inputManager.learn(output.score);
            }
        },
        1000 / ITERATIONS_PER_SECOND)
}

function evaluateManual(resolve, reject, inputManager) {

    // Init objects
    var character = new Character();
    var world = new World(worldWidth, worldHeight, character);
    var game = new Game(world, character);
    inputManager.setWorldVariables(character, world);
    inputManager.game = game;

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

            if(output.has_fallen == true) {
                score = output.score;
            }
        },
        1000 / ITERATIONS_PER_SECOND)
}

function evaluateNN(resolve, reject, inputManager, iterations, counter=0) {
    // Init objects
    var character = new Character();
    var world = new World(worldWidth, worldHeight, character);
    var game = new Game(world, character);
    inputManager.setWorldVariables(character, world, game);

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
    var lastDistance = character.getHipBaseX();
    var lastDDistance = character.getHipBaseX();
    var gameIntervalId = setInterval(
        function() {
            output = game.run(world, character, inputManager);
            if (!REWARD_AFTER_EACH_SIM) {
                var dDistance = character.getHipBaseX() - lastDistance;
                var ddDistance = dDistance - lastDDistance;
                // console.log(0.1 * distanceAccum, dDistance, ddDistance);
                // Want to penalize it for not moving forward
                var speedPenalty = 0;
                if (Math.abs(ddDistance) < 0.01)
                    speedPenalty = -5;
                inputManager.learn(dDistance + ddDistance + speedPenalty);
                lastDDistance = dDistance;
                lastDistance = character.getHipBaseX();
            }
            inputManager.visSelf(document.getElementById("netvis"));
            if(output.has_fallen == true || game.elapsedTime > NN_RUNTIME) {
                var reward = character.getHipBaseX();
                if (REWARD_AFTER_EACH_SIM) {
                    if (output.has_fallen == true) reward = reward - 500.0;
                    inputManager.learn(reward);
                }
                clearInterval(gameIntervalId);
                if(DISPLAY) { clearInterval(displayIntervalId) }
                if (counter == iterations) {
                    resolve(output.score);
                } else {
                    printOutput(counter + ', ' + output.score + ', ' + game.elapsedTime);
                    drawGraph(counter, inputManager.getSmoothedReward());
                    evaluateNN(resolve, reject, inputManager, iterations, counter + 1);
                }
            }
        },
        1000 / ITERATIONS_PER_SECOND)
}