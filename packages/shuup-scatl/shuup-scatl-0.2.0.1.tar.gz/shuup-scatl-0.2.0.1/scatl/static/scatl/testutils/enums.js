"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
function getSampleFromEnum(enumClass) {
    let enumKeys = [];
    for (let enumKey in enumClass) {
        let enumValue = enumClass[enumKey];
        if (typeof enumValue === 'number') {
            enumKeys.push(enumKey);
        }
    }
    let enumKeyIndexRandom = faker.random.number({
        min: 0,
        max: enumKeys.length - 1,
    });
    let enumKeyRandom = enumKeys[enumKeyIndexRandom];
    let enumValueRandom = enumClass[enumKeyRandom];
    return enumValueRandom;
}
exports.getSampleFromEnum = getSampleFromEnum;
//# sourceMappingURL=enums.js.map