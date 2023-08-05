import {TestBed} from '@angular/core/testing'
import {ComponentFixture} from '@angular/core/testing'
import {QueryData} from 'app/shared/query-data/query-data.model'
import {QueryDataGenerator} from 'testutils/generators/query-data'
import {DebugElement} from '@angular/core'
import {BrowserModule} from '@angular/platform-browser'
import {FormsModule} from '@angular/forms'
import {ReactiveFormsModule} from '@angular/forms'
import {NouisliderModule} from 'ng2-nouislider'
import {Component} from '@angular/core'
import {PaginationFormComponent} from 'app/product-list/pagination-form/pagination-form.comp'
import {By} from '@angular/platform-browser'
import {PageNum} from 'app/shared/query-data/query-data.model'
import {PageRangeComponent} from 'app/product-list/pagination-form/page-range.comp'
import {PageRangeService} from 'app/product-list/pagination-form/page-range.service'
import {initDjangoEnv} from 'testutils/mocks/django-env'


describe('pagination', () => {
    let self: {
        compFixture: ComponentFixture<ControlFormComponentMock>
        compDebug: DebugElement
        comp: PaginationFormComponent
    }

    beforeEach(async done => {
        initDjangoEnv()
        await initAngularEnv()
        initTestSuite()
        done()
    })

    async function initAngularEnv() {
        // noinspection JSUnusedGlobalSymbols,JSIgnoredPromiseFromCall
        await TestBed.configureTestingModule({
            imports: [
                BrowserModule,
                FormsModule,
                ReactiveFormsModule,
                NouisliderModule,
            ],
            declarations: [
                ControlFormComponentMock,
                PaginationFormComponent,
                PageRangeComponent,
            ],
            providers: [
                PageRangeService,
            ],
        })
            .compileComponents()
    }

    function initTestSuite() {
        let fixture = TestBed.createComponent(PaginationFormComponent)
        self = {
            compFixture: fixture,
            compDebug: fixture.debugElement,
            comp: fixture.componentInstance,
        }
        let gen = new QueryDataGenerator()
        self.comp.queryData = gen.data()
        self.compFixture.detectChanges()
    }

    it('current: 2, end: 2', async done => {
        setPaginationData({pageCurrent: 2, pageEnd: 2})
        expectButtonsRender({
            isLeftDisabled: false,
            isStartDisabled: false,
            isLeftEllipsisPresent: false,
            isRightEllipsisPresent: false,
            isRightDisabled: true,
            isEndPresent: true,
            isEndDisabled: true,
        })
        expectNoButtonDuplicates()
        done()
    })

    it('current: 1, end: 1', async done => {
        setPaginationData({pageCurrent: 1, pageEnd: 1})
        expectButtonsRender({
            isLeftDisabled: true,
            isStartDisabled: true,
            isLeftEllipsisPresent: false,
            isRightEllipsisPresent: false,
            isRightDisabled: true,
            isEndPresent: false,
            isEndDisabled: true,
        })
        expectNoButtonDuplicates()
        done()
    })

    it('current: 4, end: 6', async done => {
        setPaginationData({pageCurrent: 4, pageEnd: 6})
        expectButtonsRender({
            isLeftDisabled: false,
            isStartDisabled: false,
            isLeftEllipsisPresent: false,
            isRightEllipsisPresent: false,
            isRightDisabled: false,
            isEndPresent: false,
            isEndDisabled: false,
        })
        expectNoButtonDuplicates()
        done()
    })

    it('current: 4, end: 7', async done => {
        setPaginationData({pageCurrent: 4, pageEnd: 7})
        expectButtonsRender({
            isLeftDisabled: false,
            isStartDisabled: false,
            isLeftEllipsisPresent: false,
            isRightEllipsisPresent: false,
            isRightDisabled: false,
            isEndPresent: true,
            isEndDisabled: false,
        })
        expectNoButtonDuplicates()
        done()
    })

    it('current: 7, end: 9', async done => {
        setPaginationData({pageCurrent: 7, pageEnd: 9})
        expectButtonsRender({
            isLeftDisabled: false,
            isStartDisabled: false,
            isLeftEllipsisPresent: true,
            isRightEllipsisPresent: false,
            isRightDisabled: false,
            isEndPresent: true,
            isEndDisabled: false,
        })
        expectNoButtonDuplicates()
        done()
    })

    function setPaginationData(args: {pageCurrent: PageNum, pageEnd: PageNum}) {
        self.comp.queryData.pageCurrent = args.pageCurrent
        self.comp.queryData.pageLast = args.pageEnd
        self.compFixture.detectChanges()
    }

    function expectButtonsRender(args: {
        isLeftDisabled: boolean,
        isStartDisabled: boolean,
        isLeftEllipsisPresent: boolean,
        isEndPresent: boolean,
        isEndDisabled: boolean,
        isRightEllipsisPresent: boolean,
        isRightDisabled: boolean,
    }) {
        let pageButtonLeft = self.compDebug.query(By.css(`#previous`))
        expect(pageButtonLeft.properties[`disabled`]).toBe(args.isLeftDisabled)

        let pageButtonStart = self.compDebug.query(By.css(`#start`))
        expect(pageButtonStart.properties[`disabled`]).toBe(args.isStartDisabled)

        if (args.isEndPresent) {
            let pageButtonEnd = self.compDebug.query(By.css(`#end`))
            expect(pageButtonEnd.properties[`disabled`]).toBe(args.isEndDisabled)
        }

        let pageButtonRight = self.compDebug.query(By.css(`#next`))
        expect(pageButtonRight.properties[`disabled`]).toBe(args.isRightDisabled)
    }

    function expectNoButtonDuplicates() {
        let buttonContentSet: Set<string> = new Set()
        let buttons = self.compDebug.queryAll(By.css(`.page-button`))
        for (let button of buttons) {
            let buttonContent = button.nativeElement.innerText
            let isDuplicate = buttonContentSet.has(buttonContent)
            expect(isDuplicate).toBe(false)
            buttonContentSet.add(button.nativeElement.innerText)
        }
    }
})


@Component({
    selector: 'control-form',
    template: '<pagination-form [queryData]="queryData"></pagination-form>',
})
class ControlFormComponentMock {
    queryData: QueryData
}
