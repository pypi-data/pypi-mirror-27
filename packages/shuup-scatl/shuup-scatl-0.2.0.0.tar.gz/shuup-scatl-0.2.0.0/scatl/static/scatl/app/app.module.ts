import {NgModule} from '@angular/core'
import {FormsModule} from '@angular/forms'
import {ReactiveFormsModule} from '@angular/forms'
import {FormBuilder} from '@angular/forms'
import {BrowserModule} from '@angular/platform-browser'
import {HttpModule} from '@angular/http'
import {NouisliderModule} from 'ng2-nouislider'
import {routing} from 'app/app.routing'
import {AppComponent} from 'app/app.comp'
import {ProductListComponent} from 'app/product-list/product-list.comp'
import {ControlFormComponent} from 'app/control-form/control-form.comp'
import {QueryDataNetworkService} from 'app/shared/query-data/query-data-network.service'
import {ProductListService} from 'app/shared/product-list/product-list.service'
import {CatalogComponent} from 'app/catalog.comp'
import {AttrimFormComponent} from 'app/control-form/components/attrim-form.comp'
import {SortingFormComponent} from 'app/control-form/components/sorting-form.comp'
import {PriceRangeFormComponent} from 'app/control-form/components/price-range-form.comp'
import {PaginationFormComponent} from 'app/product-list/pagination-form/pagination-form.comp'
import {PageRangeService} from 'app/product-list/pagination-form/page-range.service'
import {QueryDataToRouteParamsSerializer} from 'app/shared/query-data/serializers/route-params'
import {RouteSnapshotToQueryDataDeserializer} from 'app/shared/query-data/deserializers/route-snapshot'
import {QueryDataToURLSearchParamsSerializer} from 'app/shared/query-data/serializers/search-params'
import {JsonToQueryDataDeserializer} from 'app/shared/query-data/deserializers/json'
import {PageRangeComponent} from 'app/product-list/pagination-form/page-range.comp'
import {QueryDataService} from 'app/shared/query-data/query-data.service'
import {NotifyService} from 'app/shared/notify.service'
import {SimpleNotificationsModule} from 'angular2-notifications'
import {SlimLoadingBarModule} from 'ng2-slim-loading-bar'
import {BrowserAnimationsModule} from '@angular/platform-browser/animations'

@NgModule({
    imports: [
        BrowserModule,
        BrowserAnimationsModule,
        FormsModule,
        HttpModule,
        ReactiveFormsModule,
        routing,
        NouisliderModule,
        SlimLoadingBarModule.forRoot(),
        SimpleNotificationsModule.forRoot(),
    ],
    declarations: [
        AppComponent,
        CatalogComponent,
        ControlFormComponent,
        AttrimFormComponent,
        SortingFormComponent,
        PriceRangeFormComponent,
        PaginationFormComponent,
        PageRangeComponent,
        ProductListComponent,
    ],
    bootstrap: [AppComponent],
    providers: [
        FormBuilder,
        NotifyService,
        ProductListService,
        PageRangeService,
        QueryDataService,
        QueryDataNetworkService,
        QueryDataToRouteParamsSerializer,
        QueryDataToURLSearchParamsSerializer,
        RouteSnapshotToQueryDataDeserializer,
        JsonToQueryDataDeserializer,
    ],
})
export class AppModule { }
