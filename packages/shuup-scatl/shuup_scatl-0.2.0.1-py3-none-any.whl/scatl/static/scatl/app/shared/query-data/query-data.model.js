"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class QueryData {
    constructor(args) {
        this.categorySlug = null;
        this.pageCurrent = 1;
        this.pageFirst = 1;
        this.pageLast = 1;
        this.attrimClsArray = args.attrimClsArray;
        this.priceRange = args.priceRange;
        this.sorting = args.sorting;
        this.categorySlug = args.categorySlug ? args.categorySlug : this.categorySlug;
        this.pageCurrent = args.pageCurrent ? args.pageCurrent : this.pageCurrent;
        this.pageLast = args.pageLast ? args.pageLast : this.pageLast;
    }
}
exports.QueryData = QueryData;
var Sorting;
(function (Sorting) {
    Sorting[Sorting["NameAZ"] = 0] = "NameAZ";
    Sorting[Sorting["NameZA"] = 1] = "NameZA";
    Sorting[Sorting["PriceMinMax"] = 2] = "PriceMinMax";
    Sorting[Sorting["PriceMaxMin"] = 3] = "PriceMaxMin";
})(Sorting = exports.Sorting || (exports.Sorting = {}));
class AttrimCls {
    constructor(args) {
        this.code = args.code;
        this.options = args.options || [];
        this.name = args.name || this.code;
    }
}
exports.AttrimCls = AttrimCls;
class AttrimOption {
    constructor(args) {
        this.isSelected = false;
        this.value = args.value;
        this.isSelected = args.isSelected || this.isSelected;
    }
}
exports.AttrimOption = AttrimOption;
var ShuupAttrType;
(function (ShuupAttrType) {
    ShuupAttrType[ShuupAttrType["BOOLEAN"] = 2] = "BOOLEAN";
})(ShuupAttrType = exports.ShuupAttrType || (exports.ShuupAttrType = {}));
class ShuupAttr {
    constructor(args) {
        this.identifier = args.identifier;
        this.type = args.type;
        this.value = args.value;
    }
}
exports.ShuupAttr = ShuupAttr;
class PriceRange {
    constructor(min, max) {
        this.min = min;
        this.max = max;
    }
}
exports.PriceRange = PriceRange;
//# sourceMappingURL=query-data.model.js.map