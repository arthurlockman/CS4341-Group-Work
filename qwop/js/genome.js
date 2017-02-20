

class Genome {

    constructor(genomeSize, mutationRate){

        this.genomeSize = genomeSize
        this.mutationRate = mutationRate
        this.moves = []
        this.counter = 0

        for(i = 0; i < genomeSize; i++){
            var move = []
            for(var j = 0; j < 4; j++){
                move.push(Math.random() > .5 ? 0 : 1)
            }
            this.moves.push(move)
        }
    }

    selectAndBreed(genomes, mutationRate){
        //choose two from genomes and return two children


        //mutate

    }

    getInput() {
        return this.moves[this.counter++]
    }

    mutate() {

        for(var i = 0; i < this.genomeSize; i++) {
            for(var j = 0; j < 4; j++) {
                if(Math.randome() < mutationRate) {
                    this.moves[i][j] = this.this.moves[i][j] == 0 ? 1 : 0
                }
            }
        }

    }

    learn() {
        // Do nothing, not NN
    }

    setWorldVariables(character, world) {
        // Do nothing, not NN
    }
}
