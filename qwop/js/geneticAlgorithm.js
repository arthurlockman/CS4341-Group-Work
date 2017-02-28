
class GeneticAlgorithm {

    constructor(genomeSize, popSize, elitismPct, scumismPct, mutationRate, evaluationFunction) {

        this.genomeSize = genomeSize;
        this.popSize = popSize;
        this.elitismPct = elitismPct;
        this.scumismPct = scumismPct;
        this.mutationRate = mutationRate;
        this.evaluationFunction = evaluationFunction;

        this.currentGen = 0;

        this.population = [];

        //create generation 0 with random values
        for(var i = 0; i < this.popSize; i++) {
            this.population.push(new Genome(this.genomeSize))
        }

    }

    prune(self, population, scores) {

        // Sort the genomes by their scores
        var arr = [];
        for(var i = 0; i < self.popSize; i++) {
            arr.push([population[i], scores[i]])
        }
        arr.sort((a, b) => (b[1] - a[1]));
        console.log(arr[0][1])

        // Make all the scores positive
        var min_score = arr[arr.length-1][1]
        for(var i = 0; i < arr.length; i++) {
            arr[i][1] = arr[i][1] - min_score
        }

        // Calculate the total score
        var totalScore = 0;
        for(var i = 0; i < arr.length; i++) {
            totalScore += arr[i][1]
        }

        // Keep the elites
        var numKeep = Math.round(self.popSize * self.elitismPct);
        var keep = [];
        for(var i = 0; i < numKeep; i++) {
            keep.push(arr[i][0])
        }

        // Purge the scum
        var numPurge = Math.round(self.popSize * self.scumismPct);
        for(var i = 0; i < numPurge; i++) {
            arr.splice(-1,1)
        }

        // Insert the elites into the next gen
        var nextGen = [];
        nextGen = nextGen.concat(keep);

        // Create next gen
        var numNextGenerationToCreate = self.popSize - numKeep;
        for(var i = 0; i < numNextGenerationToCreate; i++) {

            var genomeA, genomeB;
            //Error happens when sometimes these end up null (no idea why)

            var summedScore = 0;
            var dice = Math.random();
            for(var j = 0; j < arr.length; j++) {
                summedScore += arr[j][1] / totalScore;
                if(dice < summedScore) {
                    genomeA = arr[j][0];
                    break
                }
            }

            summedScore = 0;
            dice = Math.random();

            for (var j = 0; j < arr.length; j++) {
                summedScore += arr[j][1] / totalScore;
                if (dice < summedScore) {
                    genomeB = arr[j][0];
                    break
                }
            }

            nextGen.push(self.merge(self, genomeA, genomeB))
        }

        // Mutate
        for(var i = numKeep; i < nextGen.length; i++) {
            nextGen[i].mutate(nextGen[i], self.mutationRate)
        }

        if(nextGen.length != self.popSize) {
            console.log("Not enough children!")
        }

        for(var j = 0; j < nextGen.length; j++) {
            if(nextGen[j].genomeSize != self.genomeSize) {
                console.log("Genome size wrong!")
            }
        }

        for(var j = 0; j < keep.length; j++) {
            if(!nextGen.includes(keep[j])) {
                console.log("Elitism wrong!")
            }
        }

        // self.population = nextGen;
        this.population = nextGen;
        return nextGen;

    }

    merge(self, genomeA, genomeB) {
        var splitNum  = Math.round(Math.random() * self.genomeSize);

        var newGenome = new Genome(self.genomeSize);
        var genomeAMoves = arrayClone(genomeA.moves);
        var genomeBMoves = arrayClone(genomeB.moves);

        newGenome.moves = genomeAMoves.slice(0, splitNum).concat(genomeBMoves.slice(splitNum, genomeB.moves.length));

        return newGenome
    }

    evaluate(self) {

        var promises = [];

        for(var i = 0; i < self.popSize; i++) {
            promises.push(
                new Promise((resolve, reject) => 
                    self.evaluationFunction(resolve, reject, self.population[i])
            ))
        }

        Promise.all(promises).then(function(scores) {
            // Recursive evaluation
            self.population = self.prune(self, self.population, scores);
            self.evaluate(self)
        })
    }
}


function arrayClone(arr) {

    var i, copy;

    if( Array.isArray( arr ) ) {
        copy = arr.slice( 0 );
        for( i = 0; i < copy.length; i++ ) {
            copy[ i ] = arrayClone( copy[ i ] );
        }
        return copy;
    } else if( typeof arr === 'object' ) {
        throw 'Cannot clone array containing an object!';
    } else {
        return arr;
    }

}
