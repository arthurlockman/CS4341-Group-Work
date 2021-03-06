

class Genome {

    constructor(genomeSize){

        this.genomeSize = genomeSize
        this.moves = []
        this.counter = 0
        this.uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
            return v.toString(16);
        });

        for(i = 0; i < genomeSize; i++){
            var move = []
            for(var j = 0; j < 4; j++){
                move.push(Math.random() > .5 ? 0 : 1)
            }
            this.moves.push(move)
        }
    }

    getInput() {
        return this.moves[this.counter++]
    }

    mutate(self, mutationRate) {

        for(var i = 0; i < self.genomeSize; i++) {
            for(var j = 0; j < 4; j++) {
                if(Math.random() < mutationRate) {
                    self.moves[i][j] = (self.moves[i][j] == 0) ? 1 : 0
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

    dump() {
        let final = [];
        for (let i = 0; i < this.moves.length; i++)
        {
            let move = this.moves[i];
            let _tmp = "";
            _tmp += move[0] + "," + move[1]  + "," + move[2]  + "," + move[3];
            final.push(_tmp);
        }
        return final.join(":");
    }

    load(genomeString) {
        let moves = genomeString.split(":");
        this.moves = [];
        for (let i = 0; i < moves.length; i++)
        {
            let move = moves[i].split(',');
            this.moves.push(move);
        }
    }
}

Genome.prototype.toString = function() {
    return "Size: " + this.genomeSize + ", counter: " + this.counter + ", uuid: "
        + this.uuid + "\nMoves: " + this.moves;
};
