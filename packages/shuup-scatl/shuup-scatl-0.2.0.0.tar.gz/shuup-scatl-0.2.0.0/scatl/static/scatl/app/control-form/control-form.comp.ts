import {Component} from '@angular/core'
import {OnInit} from '@angular/core'
import {QueryDataService} from 'app/shared/query-data/query-data.service'
import {ProductListService} from 'app/shared/product-list/product-list.service'
import {ActivatedRoute} from '@angular/router'
import {asyncWithLoadingBar} from 'app/shared/decorators/async-with-loading-bar.decorator'
import {Loadable} from 'app/shared/decorators/async-with-loading-bar.decorator'
import {SlimLoadingBarService} from 'ng2-slim-loading-bar'
import {Notifiable} from 'app/shared/decorators/with-notify.decorator'
import {NotifyService} from 'app/shared/notify.service'
import {withNotify} from 'app/shared/decorators/with-notify.decorator'


@Component({
    selector: 'control-form',
    moduleId: module.id,
    templateUrl: 'control-form.comp.html',
    styleUrls: ['control-form.comp.css'],
})
export class ControlFormComponent implements OnInit, Loadable, Notifiable {
    // noinspection JSUnusedGlobalSymbols
    constructor(
        public loadingBarService: SlimLoadingBarService,
        public notifyService: NotifyService,
        protected queryDataService: QueryDataService,
        private activatedRoute: ActivatedRoute,
        private productListService: ProductListService,
    ) { }

    async ngOnInit() {
        await this.loadQueryDataFromUrl()
        await this.handleQueryDataUpdate()
    }
    
    @asyncWithLoadingBar
    async handleQueryDataUpdate() {
        await this.queryDataService.updateQueryData()
        await this.productListService.updateList()
    }

    @withNotify({onErrorMsg: {
        header: `URL error`,
        body: `Can't read the filters from the url, is the provided url correct?`,
    }})
    private loadQueryDataFromUrl() {
        this.queryDataService.initQueryDataFromPageUrl(this.activatedRoute.snapshot)
    }
}
