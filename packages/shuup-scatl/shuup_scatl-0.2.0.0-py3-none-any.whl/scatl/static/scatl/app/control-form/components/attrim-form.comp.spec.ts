import {TestBed} from '@angular/core/testing'
import {ComponentFixture} from '@angular/core/testing'
import {QueryData} from 'app/shared/query-data/query-data.model'
import {QueryDataGenerator} from 'testutils/generators/query-data'
import {By} from '@angular/platform-browser'
import {DebugElement} from '@angular/core'
import {BrowserModule} from '@angular/platform-browser'
import {FormsModule} from '@angular/forms'
import {ReactiveFormsModule} from '@angular/forms'
import {AttrimFormComponent} from 'app/control-form/components/attrim-form.comp'
import {initDjangoEnv} from 'testutils/mocks/django-env'
import {Component} from '@angular/core'
import FakerStatic = Faker.FakerStatic


declare var faker: FakerStatic


describe('attrim-form', () => {
    let self: {
        compFixture: ComponentFixture<AttrimFormComponent>
        compDebug: DebugElement
        comp: AttrimFormComponent
        dataSource: QueryData
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
            ],
            declarations: [
                ControlFormComponentMock,
                AttrimFormComponent,
            ],
        })
            .compileComponents()
    }

    function initTestSuite() {
        let fixture = TestBed.createComponent(AttrimFormComponent)
        let gen = new QueryDataGenerator()
        self = {
            compFixture: fixture,
            compDebug: fixture.debugElement,
            comp: fixture.componentInstance,
            dataSource: gen.data(),
        }
        self.comp.queryData = self.dataSource
        self.compFixture.detectChanges()
    }

    it('selects an option on user click', async done => {
        let clsWithOptToSelect = faker.random.arrayElement(self.dataSource.attrimClsArray)
        let optToSelect = faker.random.arrayElement(clsWithOptToSelect.options)
        let optToSelectIsSelectedSource: boolean = optToSelect.isSelected

        let optToChangeSelector = By.css(
            `[name='${clsWithOptToSelect.code}'][value='${optToSelect.value}']`
        )
        let optToSelectDebug = self.compDebug.query(optToChangeSelector)
        expect(optToSelectDebug).not.toBeNull()
        optToSelectDebug.nativeElement.click()

        await self.compFixture.whenStable()
        expect(optToSelect.isSelected).not.toBe(optToSelectIsSelectedSource)
        done()
    })

    @Component({
        selector: 'control-form',
        template: '<attrim-form [queryData]="queryData"></attrim-form>',
    })
    class ControlFormComponentMock {
        queryData: QueryData

        constructor() {
            let gen = new QueryDataGenerator()
            this.queryData = gen.data()
        }
    }
})
