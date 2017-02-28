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

var scoreAccumulator = 0;

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
    let newURL = window.location.href;
    if (newURL.includes('alg'))
    {
        newURL = newURL.replace(/alg=[a-z]*/g, "alg="+document.getElementById("algorithmSelector").value);
    }
    else if (newURL.includes('?'))
    {
        newURL += "&alg=" + document.getElementById("algorithmSelector").value
    } else {
        newURL += "?alg=" + document.getElementById("algorithmSelector").value
    }
    window.location.href = newURL;
});

function getCanvasWidth() {
    let windowHeight = window.innerHeight - 200;
    let textWidth = document.getElementById('outputTextBox').offsetWidth - 30;
    return (textWidth > windowHeight) ? windowHeight : textWidth;
}

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
    } if (QueryString.display) {
        if (QueryString.display == "false") {
            DISPLAY = false;
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
        document.getElementById("rewardtype").style.display = 'block';
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
        var genomeSize = NN_RUNTIME * 60;
        var popSize = 30;
        var elitismPct = 0.1;
        var scumismPct = 0.1;
        var mutationRate = 0.1;
        var evaluationFunction = evaluateGA;
        var ga = new GeneticAlgorithm(genomeSize, popSize, elitismPct, scumismPct, mutationRate, evaluationFunction);
        ga.evaluate(ga)

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

let graphCounter = 0;
function drawGraphY(y) {
    drawGraph(graphCounter, y);
    graphCounter += 1;
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
    let evt;
    if(DISPLAY) {
        display = new Display(document, getCanvasWidth(), getCanvasWidth(), world, worldWidth, worldHeight);
        evt = function (event) {
            display.setCanvasProperties(document, getCanvasWidth(), getCanvasWidth());
        };
        window.addEventListener('resize', evt);
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
                if(DISPLAY) {
                    clearInterval(displayIntervalId);
                    window.removeEventListener('resize', evt);
                }
                printOutput(1 + ', ' + score + ', ' + game.elapsedTime);
                drawGraphY(score);
                resolve(score);
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
    let evt;
    if(DISPLAY) {
        display = new Display(document, getCanvasWidth(), getCanvasWidth(), world, worldWidth, worldHeight);
        evt = function (event) {
            display.setCanvasProperties(document, getCanvasWidth(), getCanvasWidth());
        };
        window.addEventListener('resize', evt);
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
            drawGraphY(output.score);
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
    let evt;
    if(DISPLAY) {
        display = new Display(document, getCanvasWidth(), getCanvasWidth(), world, worldWidth, worldHeight);
        evt = function (event) {
            display.setCanvasProperties(document, getCanvasWidth(), getCanvasWidth());
        };
        window.addEventListener('resize', evt);
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
    var lastScore = 0;
    var gameIntervalId = setInterval(
        function() {
            output = game.run(world, character, inputManager);
            scoreAccumulator += output.score - lastScore;
            lastScore = output.score;
            if (!REWARD_AFTER_EACH_SIM) {
                inputManager.learn(scoreAccumulator);
            }
            inputManager.visSelf(document.getElementById("netvis"));
            if(output.has_fallen == true || game.elapsedTime > NN_RUNTIME) {
                var reward = character.getHipBaseX();
                if (REWARD_AFTER_EACH_SIM) {
                    if (output.has_fallen == true) reward = reward - 500.0;
                    inputManager.learn(reward);
                }
                clearInterval(gameIntervalId);
                if(DISPLAY) {
                    clearInterval(displayIntervalId);
                    window.removeEventListener('resize', evt);
                }
                if (counter == iterations) {
                    resolve(output.score);
                } else {
                    var _r = inputManager.getSmoothedReward();
                    printOutput(counter + ', ' + output.score + ', ' + game.elapsedTime + ', ' + _r);
                    drawGraph(counter, output.score);
                    evaluateNN(resolve, reject, inputManager, iterations, counter + 1);
                }
            }
        },
        1000 / ITERATIONS_PER_SECOND)
}