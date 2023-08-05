export class QueryData {
    attrimClsArray: Array<AttrimCls>
    priceRange: PriceRange

    sorting: Sorting

    categorySlug: CategorySlug | null = null

    pageCurrent: PageNum = 1
    pageFirst: PageNum = 1
    pageLast: PageNum = 1

    constructor(args: {
        attrimClsArray: Array<AttrimCls>,
        priceRange: PriceRange,
        sorting: Sorting,
        categorySlug?: CategorySlug | null,
        pageCurrent?: PageNum,
        pageLast?: PageNum,
    }) {
        this.attrimClsArray = args.attrimClsArray
        this.priceRange = args.priceRange
        this.sorting = args.sorting
        this.categorySlug = args.categorySlug ? args.categorySlug : this.categorySlug
        this.pageCurrent = args.pageCurrent ? args.pageCurrent : this.pageCurrent
        this.pageLast = args.pageLast ? args.pageLast : this.pageLast
    }
}


export enum Sorting {
    NameAZ,
    NameZA,
    PriceMinMax,
    PriceMaxMin,
}


export type CategorySlug = string


export class AttrimCls {
    code: AttrimClsCode
    options: Array<AttrimOption>
    name: string
    
    constructor(args: {
        code: AttrimClsCode,
        options?: Array<AttrimOption>,
        name?: string,
    }) {
        this.code = args.code
        this.options = args.options || []
        this.name = args.name || this.code
    }
}


export class AttrimOption {
    value: AttrimOptionValue
    isSelected: boolean = false
    
    constructor(args: {
        value: AttrimOptionValue,
        isSelected?: boolean,
    }) {
        this.value = args.value
        this.isSelected = args.isSelected || this.isSelected
    }
}


export type AttrimClsCode = string


export type AttrimOptionValue = string


export enum ShuupAttrType {
    BOOLEAN = 2
}


export type ShuupAttrValue = boolean


export class ShuupAttr {
    identifier: string
    type: ShuupAttrType
    value: ShuupAttrValue

    constructor(args: {
        identifier: AttrimOptionValue,
        type: ShuupAttrType,
        value: ShuupAttrValue,
    }) {
        this.identifier = args.identifier
        this.type = args.type
        this.value = args.value
    }
}


export class PriceRange {
    min: number
    max: number

    constructor(min: number, max: number) {
        this.min = min
        this.max = max
    }
}


export type PageNum = number
