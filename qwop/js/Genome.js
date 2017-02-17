

class Genome{

    constructor(){
        this.moves = []

        for(i = 0; i < 600; i++){
            move = []
            for(j = 0; j < 4; j++){
                move.push(Math.random() > .5)
            }
            moves.push(move)
        }
    }

    selectAndBreed(genomes, mutationRate){
        //choose two from genomes and return two children


        //mutate

    }



}
