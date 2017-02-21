
class GeneticAlgorithm {

    constructor(genomeSize, popSize, elitismPct, scumismPct, mutationRate, generations, evaluationFunction) {

        this.genomeSize = genomeSize;
        this.popSize = popSize;
        this.elitismPct = elitismPct;
        this.scumismPct = scumismPct;
        this.mutationRate = mutationRate;
        this.generations = generations;
        this.evaluationFunction = evaluationFunction;

        this.currentGen = 0;

        this.population = [];

        //create generation 0 with random values
        for(var i = 0; i < this.popSize; i++) {
            this.population.push(new Genome(this.genomeSize))
        }

    }

    prune(population, scores, GA) {

        var totalScore = scores.reduce((a, b) => a + b, 0);

        // Sort the genomes by their scores
        var arr = [];
        for(var i = 0; i < GA.popSize; i++) {
            arr.push([population[i], scores[i]])
        }
        arr.sort((a, b) => (a[1] < b[1]));

        // Keep the elites
        var numKeep = Math.round(GA.popSize * GA.elitismPct);
        var keep = [];
        for(var i = 0; i < numKeep; i++) {
            keep.push(arr[i][0])
        }

        // Purge the scum
        var numPurge = Math.round(GA.popSize * GA.scumismPct);
        for(var i = 0; i < numPurge; i++) {
            arr.splice(-1,1)
        }

        // Insert the elites into the next gen
        var nextGen = [];
        nextGen = nextGen.concat(keep);

        // Create next gen
        var numNextGenerationToCreate = GA.popSize - numKeep;
        for(var i = 0; i < numNextGenerationToCreate; i++) {

            var genomeA, genomeB;

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

            for(var j = 0; j < arr.length; j++) {
                summedScore += arr[j][1] / totalScore;
                if(dice < summedScore) {
                    genomeB = arr[j][0];
                    break
                }
            }

            nextGen.push(GA.merge(genomeA, genomeB, GA))
        }

        // Mutate
        for(var i = numKeep; i < nextGen.length; i++) {
            nextGen[i].mutate(nextGen[i], GA.mutationRate)
        }

        return nextGen

    }

    merge(genomeA, genomeB, GA) {

        var splitNum  = Math.round(Math.random() * GA.genomeSize);

        var newGenome = new Genome(GA.genomeSize);
        var genomeAMoves = arrayClone(genomeA.moves)
        var genomeBMoves = arrayClone(genomeB.moves)

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

        Promise.all(promises).then((scores) => self.prune(self.population, scores, self))
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
