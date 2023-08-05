import {TestBed} from '@angular/core/testing'
import {ComponentFixture} from '@angular/core/testing'
import {QueryData} from 'app/shared/query-data/query-data.model'
import {QueryDataGenerator} from 'testutils/generators/query-data'
import {By} from '@angular/platform-browser'
import {DebugElement} from '@angular/core'
import {BrowserModule} from '@angular/platform-browser'
import {FormsModule} from '@angular/forms'
import {ReactiveFormsModule} from '@angular/forms'
import {NouisliderModule} from 'ng2-nouislider'
import {NouisliderComponent} from 'ng2-nouislider'
import {PriceRangeFormComponent} from 'app/control-form/components/price-range-form.comp'
import {Component} from '@angular/core'
import {initDjangoEnv} from 'testutils/mocks/django-env'


describe('price-range', () => {
    let self: {
        compFixture: ComponentFixture<ControlFormComponentMock>
        compDebug: DebugElement
        comp: PriceRangeFormComponent
    }

    beforeEach(async done => {
        initDjangoEnv()
        await initAngularEnv()
        initTestSuite()
        done()
    })

    async function initAngularEnv() {
        await TestBed.configureTestingModule({
            imports: [
                BrowserModule,
                FormsModule,
                ReactiveFormsModule,
                NouisliderModule,
            ],
            declarations: [
                ControlFormComponentMock,
                PriceRangeFormComponent,
            ],
        })
            .compileComponents()
    }

    function initTestSuite() {
        let fixture = TestBed.createComponent(PriceRangeFormComponent)
        self = {
            compFixture: fixture,
            compDebug: fixture.debugElement,
            comp: fixture.componentInstance,
        }
        let gen = new QueryDataGenerator()
        self.comp.queryData = gen.data()
        self.compFixture.detectChanges()
    }

    it('changes the `min` priceRange input', () => {
        testPriceRangeUpdate('min')
    })

    it('changes the `max` priceRange input', () => {
        testPriceRangeUpdate('max')
    })

    it('syncs the price range inputs with the slider', () => {
        let sliderDebug = self.compDebug.query(By.directive(NouisliderComponent))
        let sliderInstance = sliderDebug.componentInstance
        let priceRangeMin = 200
        let priceRangeMax = 15000
        sliderInstance.slider.set([priceRangeMin, priceRangeMax])
        self.compFixture.detectChanges()

        let priceRangeMinDebug: DebugElement = self.compDebug.query(
            By.css(`input[name='price-min']`),
        )
        expect(priceRangeMinDebug.properties['value']).toBe(priceRangeMin)

        let priceRangeMaxDebug: DebugElement = self.compDebug.query(
            By.css(`input[name='price-max']`),
        )
        expect(priceRangeMaxDebug.properties['value']).toBe(priceRangeMax)
    })

    it('syncs the price range slider with the inputs', () => {
        let priceRangeMin = 200
        let priceRangeMax = 15000
        setInputValue({name: `price-min`, value: priceRangeMin})
        setInputValue({name: `price-max`, value: priceRangeMax})
        self.compFixture.detectChanges()
        expect(self.comp.formGroup.value).toEqual({
            slider: [priceRangeMin, priceRangeMax],
            priceMin: priceRangeMin,
            priceMax: priceRangeMax,
        })
    })

    function testPriceRangeUpdate(priceRangeInput: string) {
        let priceRangeInputValue = 1000
        setInputValue({
            name: `price-${priceRangeInput}`,
            value: priceRangeInputValue,
        })
        self.compFixture.detectChanges()
        let priceRangeValue = self.comp.queryData.priceRange!![priceRangeInput]
        expect(priceRangeValue).toBe(priceRangeInputValue)
    }

    function setInputValue(args: {name: string, value: any}) {
        let inputDebug: DebugElement = self.compDebug.query(
            By.css(`input[name='${args.name}']`),
        )
        inputDebug.nativeElement.value = args.value
        let changeEvent = createEvent('change')
        inputDebug.nativeElement.dispatchEvent(changeEvent)
    }

    function createEvent(eventName: string): CustomEvent {
        let event = document.createEvent('CustomEvent')
        event.initCustomEvent(eventName, false, false, null)
        return event
    }

    @Component({
        selector: 'control-form',
        template: '<price-range-form [queryData]="queryData"></price-range-form>',
    })
    class ControlFormComponentMock {
        queryData: QueryData
    }
})
