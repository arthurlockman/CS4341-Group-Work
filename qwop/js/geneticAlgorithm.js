
class GenerticAlgorithm {

    constructor(genomeSize, popSize, elitismPct, mutationRate, generations, evaluationFunction) {

        this.genomeSize = genomeSize
        this.popSize = popSize
        this.elitismPct = elitismPct
        this.mutationRate = mutationRate
        this.generations = generations
        this.evaluationFunction = evaluationFunction

        this.currentGen = 0

        this.population = []

        //create generation 0 with random values
        for(var i = 0; i < this.popSize; i++){
            this.population.push(new Genome(this.genomeSize, this.mutationRate))
        }

        this.evaluate(this.prune)

    }

    // run(){

    //     while(this.currentGen < this.generations){
    //         //assign fitnesses
    //         //TODO
    //         genomes = []


    //         newPopulation = []

    //         //elitism
    //         if(this.elitismPct > 0) {
    //             //sort
    //             //TODO

    //             eliteIndex = floor(this.popSize * this.elitismPct)+1
    //             elites = genomes.slice(0, eliteIndex)

    //             newPopulation.push(elites)
    //         }

    //         //breed
    //         while(newPopulation.length < this.popSize){
    //             //select which two genomes to breed and breed them
    //             //also mutate
    //             newPopulation.push(Genome.selectAndBreed(genomes, this.mutationRate))
    //         }

    //         this.current_gen++
    //     }

    //     //return best Genome? return score?
    //     //TODO

    // }

    prune(population, scores) {

        var arr = []
        for(var i = 0; i < this.popSize; i++) {
            arr.push([population[i], scores[i]])
        }

        arr.sort(function(a, b) {return (a[1] > b[1])})

        console.log(arr)


    }

    evaluate(pruneFunction) {

        var promises = []

        for(var i = 0; i < this.popSize; i++) {
            genomes.push(new Genome(this.genomeSize, 0.1))
            promises.push(
                new Promise((resolve, reject) => 
                    this.evaluationFunction(resolve, reject, genomes[i])
            ))
        }

        Promise.all(promises).then((scores) => pruneFunction(this.population, scores))
    }

}
