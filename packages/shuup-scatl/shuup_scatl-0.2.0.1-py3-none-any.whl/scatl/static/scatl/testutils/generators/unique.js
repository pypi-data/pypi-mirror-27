"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class UniqueGenerator {
    constructor() {
        this.fake = faker;
        this.wordsGenerated = [];
    }
    word() {
        let iterationLimit = 2500;
        let iterationCount = 0;
        while (true) {
            let word = this.fake.lorem.word();
            let isWordUnique = !this.wordsGenerated.includes(word);
            if (isWordUnique) {
                this.wordsGenerated.push(word);
                return word;
            }
            iterationCount++;
            if (iterationCount > iterationLimit) {
                throw new Error('The unique gen is unable to generate any more unique values');
            }
        }
    }
}
exports.UniqueGenerator = UniqueGenerator;
//# sourceMappingURL=unique.js.map