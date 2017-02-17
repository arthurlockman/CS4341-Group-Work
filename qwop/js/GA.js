
class GA {

    constructor(genomeSize, popSize, elitismPct, mutationRate, generations) {

        this.genomeSize = genomeSize
        this.popSize = popSize
        this.elitismPct = elitismPct
        this.mutationRate = mutationRate
        this.generations = generations

        this.currentGen = 0

        this.population = []

        //create generation 0 with random values
        for(var i = 0; i < this.popSize; i++){
            this.population.push(new Genome(this.genomeSize, this.mutationRate))
        }

    }

    run(){


        //loop
        while(this.currentGen < this.generations){
            //assign fitnesses
            //TODO
            genomes = []


            newPopulation = []

            //elitism
            if(this.elitismPct > 0) {
                //sort
                //TODO

                eliteIndex = floor(this.popSize * this.elitismPct)+1
                elites = genomes.slice(0, eliteIndex)

                newPopulation.push(elites)
            }

            //breed
            while(newPopulation.length < this.popSize){
                //select which two genomes to breed and breed them
                //also mutate
                newPopulation.push(Genome.selectAndBreed(genomes, this.mutationRate))
            }

            this.current_gen++
        }

        //return best Genome? return score?
        //TODO




    }

}