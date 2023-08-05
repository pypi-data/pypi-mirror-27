import {Injectable} from '@angular/core'
import {QueryData} from 'app/shared/query-data/query-data.model'
import {Router} from '@angular/router'
import {RouteSnapshotToQueryDataDeserializer} from 'app/shared/query-data/deserializers/route-snapshot'
import {QueryDataToRouteParamsSerializer} from 'app/shared/query-data/serializers/route-params'
import {QueryDataNetworkService} from 'app/shared/query-data/query-data-network.service'
import {ActivatedRouteSnapshot} from '@angular/router'
import {asyncWithNotify} from 'app/shared/decorators/with-notify.decorator'
import {Notifiable} from 'app/shared/decorators/with-notify.decorator'
import {NotifyService} from 'app/shared/notify.service'


@Injectable()
export class QueryDataService implements Notifiable {
    queryData: QueryData
    
    private queryDataPromise: Promise<QueryData>
    
    // noinspection JSUnusedGlobalSymbols
    constructor(
        public notifyService: NotifyService,
        private router: Router,
        private queryDataNetworkService: QueryDataNetworkService,
        private routeSnapshotDeserializer: RouteSnapshotToQueryDataDeserializer,
        private routeParamsSerializer: QueryDataToRouteParamsSerializer,
    ) { }

    /**
     * It must receive ActivatedRouteSnapshot externally because otherwise
     * angular will inject in service only the default root routers, while
     * here it needs the current one.
     */
    initQueryDataFromPageUrl(routeSnapshot: ActivatedRouteSnapshot) {
        this.queryData = this.routeSnapshotDeserializer.toQueryData(routeSnapshot)
    }
    
    @asyncWithNotify({onErrorMsg: {header: `Filters update error`}})
    async updateQueryData() {
        this.updatePageUrlAccordingToQueryData()
        await this.updateQueryDataFromServer()
    }

    private updatePageUrlAccordingToQueryData() {
        let queryDataParamsNew = this.routeParamsSerializer.toRouteParams(this.queryData)
        let currentRouterLocation = `.`
        // noinspection JSIgnoredPromiseFromCall
        this.router.navigate([currentRouterLocation, queryDataParamsNew])
    }

    private updateQueryDataFromServer(): Promise<QueryData> {
        this.rejectPromise(this.queryDataPromise)
        this.queryDataPromise = this.queryDataNetworkService.update(this.queryData)
        this.queryDataPromise.then(qs => this.queryData = qs)
        return this.queryDataPromise
    }
    
    private rejectPromise(promise: Promise<QueryData> | undefined) {
        if (promise === undefined) {
            return
        }
        let returnOldQueryData = () => this.queryData
        promise.then(returnOldQueryData)
    }
}
