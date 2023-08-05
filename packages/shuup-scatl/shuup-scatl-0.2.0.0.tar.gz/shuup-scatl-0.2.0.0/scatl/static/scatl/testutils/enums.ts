import FakerStatic = Faker.FakerStatic


declare var faker: FakerStatic


export function getSampleFromEnum(enumClass: Object): number {
    let enumKeys: Array<string> = []
    for (let enumKey in enumClass) {
        let enumValue: number | string = enumClass[enumKey]
        if (typeof enumValue === 'number') {
            enumKeys.push(enumKey)
        }
    }
    let enumKeyIndexRandom = faker.random.number({
        min: 0,
        max: enumKeys.length - 1,
    })
    let enumKeyRandom: string = enumKeys[enumKeyIndexRandom]
    let enumValueRandom: number = enumClass[enumKeyRandom]
    return enumValueRandom
}
