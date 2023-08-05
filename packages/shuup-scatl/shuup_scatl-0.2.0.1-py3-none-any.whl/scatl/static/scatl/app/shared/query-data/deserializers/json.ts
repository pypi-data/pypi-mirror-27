import {AttrimCls} from 'app/shared/query-data/query-data.model'
import {AttrimOption} from 'app/shared/query-data/query-data.model'
import {QueryData} from 'app/shared/query-data/query-data.model'
import {Injectable} from '@angular/core'


@Injectable()
export class JsonToQueryDataDeserializer {
    toQueryData(args: {dataJson: any, dataInitial: QueryData}): QueryData {
        // TODO what about the other initial data? it does not require deserialization?
        let queryData = args.dataInitial
        queryData.attrimClsArray = this.deserializeAttrimClsArray(args.dataJson)
        queryData.pageLast = args.dataJson.page_last
        return queryData
    }

    private deserializeAttrimClsArray(json: any): Array<AttrimCls> {
        let clsArray: Array<AttrimCls> = []
        let clsJsonArray = json.attrim_cls_list
        for (let clsJson of clsJsonArray) {
            let options: Array<AttrimOption> = []
            for (let optionJson of clsJson.options) {
                let option = new AttrimOption({
                    value: optionJson.value,
                    isSelected: optionJson.is_selected,
                })
                options.push(option)
            }

            let cls = new AttrimCls({
                code: clsJson.code,
                name: clsJson.name,
                options: options,
            })
            clsArray.push(cls)
        }
        return clsArray
    }
}
