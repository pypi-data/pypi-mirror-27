import {TestBed} from '@angular/core/testing'
import {ComponentFixture} from '@angular/core/testing'
import {ControlFormComponent} from 'app/control-form/control-form.comp'
import {QueryData} from 'app/shared/query-data/query-data.model'
import {ProductListService} from 'app/shared/product-list/product-list.service'
import {QueryDataNetworkService} from 'app/shared/query-data/query-data-network.service'
import {ActivatedRoute} from '@angular/router'
import {Router} from '@angular/router'
import {QueryDataGenerator} from 'testutils/generators/query-data'
import {By} from '@angular/platform-browser'
import {DebugElement} from '@angular/core'
import {AttrimOption} from 'app/shared/query-data/query-data.model'
import {Sorting} from 'app/shared/query-data/query-data.model'
import {BrowserModule} from '@angular/platform-browser'
import {FormsModule} from '@angular/forms'
import {ReactiveFormsModule} from '@angular/forms'
import {NouisliderModule} from 'ng2-nouislider'
import {AttrimFormComponent} from 'app/control-form/components/attrim-form.comp'
import {SortingFormComponent} from 'app/control-form/components/sorting-form.comp'
import {PriceRangeFormComponent} from 'app/control-form/components/price-range-form.comp'
import {initDjangoEnv} from 'testutils/mocks/django-env'
import {RouteSnapshotToQueryDataDeserializer} from 'app/shared/query-data/deserializers/route-snapshot'
import {QueryDataToRouteParamsSerializer} from 'app/shared/query-data/serializers/route-params'
import {QueryDataService} from 'app/shared/query-data/query-data.service'
import {SlimLoadingBarService} from 'ng2-slim-loading-bar'
import {NotifyService} from 'app/shared/notify.service'
import {SimpleNotificationsModule} from 'angular2-notifications'


describe('control-form', () => {
    let self: {
        compFixture: ComponentFixture<ControlFormComponent>
        compDebug: DebugElement
        comp: ControlFormComponent
        dataSource: QueryData
        queryDataService: QueryDataService
    }

    beforeEach(async done => {
        initDjangoEnv()
        await initAngularEnv()
        initTestSuite()
        done()
    })

    async function initAngularEnv() {
        // noinspection JSUnusedGlobalSymbols
        await TestBed.configureTestingModule({
            imports: [
                BrowserModule,
                FormsModule,
                ReactiveFormsModule,
                NouisliderModule,
                SimpleNotificationsModule.forRoot(),
            ],
            declarations: [
                ControlFormComponent,
                SortingFormComponent,
                AttrimFormComponent,
                PriceRangeFormComponent,
            ],
            providers: [
                {provide: RouteSnapshotToQueryDataDeserializer, useValue: {},},
                {provide: QueryDataToRouteParamsSerializer, useValue: {},},
                {provide: Router, useValue: {},},
                {provide: ProductListService, useValue: {},},
                {provide: QueryDataNetworkService, useValue: {},},
                {provide: ActivatedRoute, useValue: {},},
                NotifyService,
                QueryDataService,
                SlimLoadingBarService,
            ],
        })
            .compileComponents()
    }

    function initTestSuite() {
        let fixture = TestBed.createComponent(ControlFormComponent)
        let gen = new QueryDataGenerator()
        self = {
            compFixture: fixture,
            compDebug: fixture.debugElement,
            comp: fixture.componentInstance,
            dataSource: gen.data(),
            queryDataService: TestBed.get(QueryDataService),
        }

        // `callFake` because `callThrough` doesn't work
        // (jasmine core 2.7.0, angular 5.0.1)
        spyOn(self.comp as any, 'ngOnInit').and.callFake(() => {})
        spyOn(self.comp as any, 'handleQueryDataUpdate').and.callFake(() => {})

        self.queryDataService.queryData = self.dataSource
        self.compFixture.detectChanges()
    }

    it('renders expected values', () => {
        let sortingCheckedSelector = By.css(`input[name='sorting']:checked`)
        let sortingChecked: DebugElement | null = self.compDebug.query(sortingCheckedSelector)
        expect(sortingChecked.properties['value']).toBe(self.dataSource.sorting)

        for (let clsSource of self.dataSource.attrimClsArray) {
            let optionSelector = By.css(`input[name='${clsSource.code}']`)
            let optionsRendered = self.compDebug.queryAll(optionSelector)
            for (let optionRendered of optionsRendered) {
                let isOptionSource = (option: AttrimOption): boolean => {
                    return option.value === optionRendered.properties['value']
                }
                let optionSource = clsSource.options.find(isOptionSource)!!
                expect(optionRendered.properties['checked']).toBe(optionSource.isSelected)
            }
        }
    })

    for (let arg of [
        {sortingOld: Sorting.NameAZ,      sortingNew: Sorting.PriceMaxMin},
        {sortingOld: Sorting.NameZA,      sortingNew: Sorting.PriceMaxMin},
        {sortingOld: Sorting.PriceMaxMin, sortingNew: Sorting.PriceMinMax},
    ]) {
        it(`updates the sorting (from ${arg.sortingOld} to ${arg.sortingNew})`, async done => {
            setComponentSorting(arg.sortingOld)
            expect(self.queryDataService.queryData.sorting).toBe(arg.sortingOld)

            await selectSorting(arg.sortingNew)
            expect(self.queryDataService.queryData.sorting).toBe(arg.sortingNew)

            done()
        })
    }

    it('inits the price range', () => {
        expect(self.queryDataService.queryData.priceRange.min).toBe(self.dataSource.priceRange.min)
        expect(self.queryDataService.queryData.priceRange.max).toBe(self.dataSource.priceRange.max)
    })

    function setComponentSorting(sortingNew: Sorting) {
        self.queryDataService.queryData.sorting = sortingNew
        self.compFixture.detectChanges()
    }

    async function selectSorting(sorting: Sorting) {
        let sortingNewSelector = By.css(
            `input[name='sorting'][value='${sorting}']`
        )
        let sortingNewDebug = self.compDebug.query(sortingNewSelector)
        let sortingNewElem: HTMLElement = sortingNewDebug.nativeElement
        sortingNewElem.click()
        await self.compFixture.whenStable()
    }
})
