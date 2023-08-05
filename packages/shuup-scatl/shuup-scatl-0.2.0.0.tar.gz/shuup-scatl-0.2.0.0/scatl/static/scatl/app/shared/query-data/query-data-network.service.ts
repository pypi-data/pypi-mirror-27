import {Injectable} from '@angular/core'
import {Http} from '@angular/http'
import {Response} from '@angular/http'
import {QueryData} from 'app/shared/query-data/query-data.model'
import {QueryDataToURLSearchParamsSerializer} from 'app/shared/query-data/serializers/search-params'
import {JsonToQueryDataDeserializer} from 'app/shared/query-data/deserializers/json'


@Injectable()
export class QueryDataNetworkService {
    private url = `/api/scatl/front/query-data/`

    constructor(
        private http: Http,
        private queryDataSerializer: QueryDataToURLSearchParamsSerializer,
        private queryDataDeserializer: JsonToQueryDataDeserializer,
    ) { }

    async update(queryData: QueryData): Promise<QueryData> {
        let params = this.queryDataSerializer.toSearchParams(queryData)
        let observable = this.http.get(this.url, {search: params})
            .retry(2)
            .map(
                (response: Response): QueryData => {
                    return this.queryDataDeserializer.toQueryData({
                        dataJson: response.json(),
                        dataInitial: queryData,
                    })
                }
            )
        return observable.toPromise()
    }
}
