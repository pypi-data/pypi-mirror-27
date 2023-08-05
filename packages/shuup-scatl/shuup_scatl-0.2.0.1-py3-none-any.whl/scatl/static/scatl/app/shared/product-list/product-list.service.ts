import {Injectable} from '@angular/core'
import {Http} from '@angular/http'
import {Product} from 'app/shared/product-list/product.model'
import {deserializeProductList} from 'app/shared/product-list/deserializers/json'
import {QueryDataToURLSearchParamsSerializer} from 'app/shared/query-data/serializers/search-params'
import {QueryDataService} from 'app/shared/query-data/query-data.service'
import {asyncWithNotify} from 'app/shared/decorators/with-notify.decorator'
import {Notifiable} from 'app/shared/decorators/with-notify.decorator'
import {NotifyService} from 'app/shared/notify.service'


@Injectable()
export class ProductListService implements Notifiable {
    productList: Array<Product>

    private productListUrl = `/api/scatl/front/products/`
    private productListPromise: Promise<Array<Product>>

    // noinspection JSUnusedGlobalSymbols
    constructor(
        public notifyService: NotifyService,
        private http: Http,
        private paramsSerializer: QueryDataToURLSearchParamsSerializer,
        private queryDataService: QueryDataService,
    ) { }

    async updateList() {
        this.rejectPromise(this.productListPromise)
        this.productList = await this.getProductList()
    }

    @asyncWithNotify({onErrorMsg: {header: `Product list update error`}})
    private async getProductList(): Promise<Array<Product>> {
        let params = this.paramsSerializer.toSearchParams(this.queryDataService.queryData)
        let productListObservable = this.http
            .get(this.productListUrl, {search: params})
            .map(deserializeProductList)
        this.productListPromise = productListObservable.toPromise()
        return this.productListPromise
    }
    
    private rejectPromise(promise: Promise<Array<Product>> | undefined) {
        if (promise === undefined) {
            return
        }
        let returnOldProductList = () => this.productList
        promise.then(returnOldProductList)
    }
}
