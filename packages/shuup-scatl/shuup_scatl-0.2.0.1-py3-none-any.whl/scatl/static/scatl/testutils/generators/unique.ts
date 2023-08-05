import FakerStatic = Faker.FakerStatic


declare var faker: FakerStatic


export class UniqueGenerator {
    private fake: FakerStatic
    // noinspection JSMismatchedCollectionQueryUpdate
    private wordsGenerated: Array<string>

    constructor() {
        this.fake = faker
        this.wordsGenerated = []
    }

    word(): string {
        let iterationLimit = 2500
        let iterationCount = 0
        while (true) {
            let word = this.fake.lorem.word()
            let isWordUnique = !(this.wordsGenerated as any).includes(word)
            if (isWordUnique) {
                this.wordsGenerated.push(word)
                return word
            }
            iterationCount++
            if (iterationCount > iterationLimit) {
                throw new Error(
                    'The unique gen is unable to generate any more unique values'
                )
            }
        }
    }
}
