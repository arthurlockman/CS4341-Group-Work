
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

        var totalScore = 0
        for(var i = 0; i < scores.length; i++) {
            totalScore += scores[i]
        }
        

        // Sort the genomes by their scores
        var arr = [];
        for(var i = 0; i < self.popSize; i++) {
            arr.push([population[i], scores[i]])
        }
        arr.sort((a, b) => (b[1] - a[1]));
        console.log(arr[0]);

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

            var summedScore = 0;
            var dice = Math.random();
            while (genomeA == undefined)
            {
                summedScore = 0;
                dice = Math.random();
                for(var j = 0; j < arr.length; j++) {
                    summedScore += arr[j][1] / totalScore;
                    if(dice < summedScore) {
                        genomeA = arr[j][0];
                        break
                    }
                }
            }

            while (genomeB == undefined) {
                summedScore = 0;
                dice = Math.random();

                for (var j = 0; j < arr.length; j++) {
                    summedScore += arr[j][1] / totalScore;
                    if (dice < summedScore) {
                        genomeB = arr[j][0];
                        break
                    }
                }
            }

            nextGen.push(self.merge(self, genomeA, genomeB))
        }

        // Mutate
        for(var i = numKeep; i < nextGen.length; i++) {
            nextGen[i].mutate(nextGen[i], self.mutationRate)
        }

        self.population = nextGen;
        // return nextGen

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
            self.prune(self, self.population, scores)

            // Recursive evaluation
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
