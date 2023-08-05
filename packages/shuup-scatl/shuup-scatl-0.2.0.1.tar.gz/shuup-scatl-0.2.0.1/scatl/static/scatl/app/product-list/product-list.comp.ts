import {Component} from '@angular/core'
import {ProductListService} from 'app/shared/product-list/product-list.service'
import {QueryDataService} from 'app/shared/query-data/query-data.service'


declare var window: Window


@Component({
    selector: 'product-list',
    moduleId: module.id,
    templateUrl: 'product-list.comp.html',
    styleUrls: ['product-list.comp.css'],
})
export class ProductListComponent {
    constructor(
        protected queryDataService: QueryDataService,
        protected productListService: ProductListService
    ) { }
    
    async handlePageFormUpdate() {
        await this.queryDataService.updateQueryData()
        this.productListService.updateList()
    }
}
