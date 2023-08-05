"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const testing_1 = require("@angular/core/testing");
const query_data_1 = require("testutils/generators/query-data");
const platform_browser_1 = require("@angular/platform-browser");
const forms_1 = require("@angular/forms");
const forms_2 = require("@angular/forms");
const ng2_nouislider_1 = require("ng2-nouislider");
const core_1 = require("@angular/core");
const pagination_form_comp_1 = require("app/product-list/pagination-form/pagination-form.comp");
const platform_browser_2 = require("@angular/platform-browser");
const page_range_comp_1 = require("app/product-list/pagination-form/page-range.comp");
const page_range_service_1 = require("app/product-list/pagination-form/page-range.service");
const django_env_1 = require("testutils/mocks/django-env");
describe('pagination', () => {
    let self;
    beforeEach((done) => __awaiter(this, void 0, void 0, function* () {
        django_env_1.initDjangoEnv();
        yield initAngularEnv();
        initTestSuite();
        done();
    }));
    function initAngularEnv() {
        return __awaiter(this, void 0, void 0, function* () {
            // noinspection JSUnusedGlobalSymbols,JSIgnoredPromiseFromCall
            yield testing_1.TestBed.configureTestingModule({
                imports: [
                    platform_browser_1.BrowserModule,
                    forms_1.FormsModule,
                    forms_2.ReactiveFormsModule,
                    ng2_nouislider_1.NouisliderModule,
                ],
                declarations: [
                    ControlFormComponentMock,
                    pagination_form_comp_1.PaginationFormComponent,
                    page_range_comp_1.PageRangeComponent,
                ],
                providers: [
                    page_range_service_1.PageRangeService,
                ],
            })
                .compileComponents();
        });
    }
    function initTestSuite() {
        let fixture = testing_1.TestBed.createComponent(pagination_form_comp_1.PaginationFormComponent);
        self = {
            compFixture: fixture,
            compDebug: fixture.debugElement,
            comp: fixture.componentInstance,
        };
        let gen = new query_data_1.QueryDataGenerator();
        self.comp.queryData = gen.data();
        self.compFixture.detectChanges();
    }
    it('current: 2, end: 2', (done) => __awaiter(this, void 0, void 0, function* () {
        setPaginationData({ pageCurrent: 2, pageEnd: 2 });
        expectButtonsRender({
            isLeftDisabled: false,
            isStartDisabled: false,
            isLeftEllipsisPresent: false,
            isRightEllipsisPresent: false,
            isRightDisabled: true,
            isEndPresent: true,
            isEndDisabled: true,
        });
        expectNoButtonDuplicates();
        done();
    }));
    it('current: 1, end: 1', (done) => __awaiter(this, void 0, void 0, function* () {
        setPaginationData({ pageCurrent: 1, pageEnd: 1 });
        expectButtonsRender({
            isLeftDisabled: true,
            isStartDisabled: true,
            isLeftEllipsisPresent: false,
            isRightEllipsisPresent: false,
            isRightDisabled: true,
            isEndPresent: false,
            isEndDisabled: true,
        });
        expectNoButtonDuplicates();
        done();
    }));
    it('current: 4, end: 6', (done) => __awaiter(this, void 0, void 0, function* () {
        setPaginationData({ pageCurrent: 4, pageEnd: 6 });
        expectButtonsRender({
            isLeftDisabled: false,
            isStartDisabled: false,
            isLeftEllipsisPresent: false,
            isRightEllipsisPresent: false,
            isRightDisabled: false,
            isEndPresent: false,
            isEndDisabled: false,
        });
        expectNoButtonDuplicates();
        done();
    }));
    it('current: 4, end: 7', (done) => __awaiter(this, void 0, void 0, function* () {
        setPaginationData({ pageCurrent: 4, pageEnd: 7 });
        expectButtonsRender({
            isLeftDisabled: false,
            isStartDisabled: false,
            isLeftEllipsisPresent: false,
            isRightEllipsisPresent: false,
            isRightDisabled: false,
            isEndPresent: true,
            isEndDisabled: false,
        });
        expectNoButtonDuplicates();
        done();
    }));
    it('current: 7, end: 9', (done) => __awaiter(this, void 0, void 0, function* () {
        setPaginationData({ pageCurrent: 7, pageEnd: 9 });
        expectButtonsRender({
            isLeftDisabled: false,
            isStartDisabled: false,
            isLeftEllipsisPresent: true,
            isRightEllipsisPresent: false,
            isRightDisabled: false,
            isEndPresent: true,
            isEndDisabled: false,
        });
        expectNoButtonDuplicates();
        done();
    }));
    function setPaginationData(args) {
        self.comp.queryData.pageCurrent = args.pageCurrent;
        self.comp.queryData.pageLast = args.pageEnd;
        self.compFixture.detectChanges();
    }
    function expectButtonsRender(args) {
        let pageButtonLeft = self.compDebug.query(platform_browser_2.By.css(`#previous`));
        expect(pageButtonLeft.properties[`disabled`]).toBe(args.isLeftDisabled);
        let pageButtonStart = self.compDebug.query(platform_browser_2.By.css(`#start`));
        expect(pageButtonStart.properties[`disabled`]).toBe(args.isStartDisabled);
        if (args.isEndPresent) {
            let pageButtonEnd = self.compDebug.query(platform_browser_2.By.css(`#end`));
            expect(pageButtonEnd.properties[`disabled`]).toBe(args.isEndDisabled);
        }
        let pageButtonRight = self.compDebug.query(platform_browser_2.By.css(`#next`));
        expect(pageButtonRight.properties[`disabled`]).toBe(args.isRightDisabled);
    }
    function expectNoButtonDuplicates() {
        let buttonContentSet = new Set();
        let buttons = self.compDebug.queryAll(platform_browser_2.By.css(`.page-button`));
        for (let button of buttons) {
            let buttonContent = button.nativeElement.innerText;
            let isDuplicate = buttonContentSet.has(buttonContent);
            expect(isDuplicate).toBe(false);
            buttonContentSet.add(button.nativeElement.innerText);
        }
    }
});
let ControlFormComponentMock = class ControlFormComponentMock {
};
ControlFormComponentMock = __decorate([
    core_1.Component({
        selector: 'control-form',
        template: '<pagination-form [queryData]="queryData"></pagination-form>',
    })
], ControlFormComponentMock);
//# sourceMappingURL=pagination-form.comp.spec.js.map