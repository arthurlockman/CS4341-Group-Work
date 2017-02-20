
class InputManager {

    constructor(document) {

        // Static reference for weird javascript scoping issues
        var self = this;

        this.keyState = 0;
        this.keyMasks = {q:1,w:2,o:4,p:8};
        this.keyEventCodes = {80:'p', 79:'o', 87:'w', 81:'q', 32:' '};

        document.onkeyup = function(event) {
            var c = self.keyEventCodes[event.keyCode];
            var m = self.keyMasks[c];
            if (m != undefined) {
                self.keyState = self.keyState & ~m
            }
        };

        /**
        * Logs the current key pressed in the keyState variable
        */
        document.onkeydown = function(event) {
            var c = self.keyEventCodes[event.keyCode];
            if (c == ' ') {
                if (self.game.elapsedTime > 1.5) {
                    self.game.resetRunner()
                }
            }
            var m = self.keyMasks[c];
            if (m != undefined) {
                self.keyState = self.keyState | m
            }
        }

    }

    // Bit shifts the keyState such that the first bit is 1 if q is pressed, 0 otherwise. Same for other keys in QWOP.
    getInput() {

        var array = [0, 0, 0, 0];
        for(var i=0; i < 4; i++) {
            array[i] = (this.keyState >> i) & 1
        }

        return array
    }

    learn() {
        // Do nothing, not NN
    }

    setWorldVariables(character, world) {
        // Do nothing, not NN
    }
}



    
