

class Genome{

    constructor(){
        this.moves = []

        for(i = 0; i < 600; i++){
            var move = []
            for(var j = 0; j < 4; j++){
                move.push(Math.random() > .5 ? 0 : 1)
            }
            this.moves.push(move)
        }

        console.log(this.moves)
    }

    selectAndBreed(genomes, mutationRate){
        //choose two from genomes and return two children


        //mutate

    }



}
