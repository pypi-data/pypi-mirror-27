"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
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
const platform_browser_2 = require("@angular/platform-browser");
const forms_1 = require("@angular/forms");
const forms_2 = require("@angular/forms");
const attrim_form_comp_1 = require("app/control-form/components/attrim-form.comp");
const django_env_1 = require("testutils/mocks/django-env");
const core_1 = require("@angular/core");
describe('attrim-form', () => {
    let self;
    beforeEach((done) => __awaiter(this, void 0, void 0, function* () {
        django_env_1.initDjangoEnv();
        yield initAngularEnv();
        initTestSuite();
        done();
    }));
    function initAngularEnv() {
        return __awaiter(this, void 0, void 0, function* () {
            // noinspection JSUnusedGlobalSymbols
            yield testing_1.TestBed.configureTestingModule({
                imports: [
                    platform_browser_2.BrowserModule,
                    forms_1.FormsModule,
                    forms_2.ReactiveFormsModule,
                ],
                declarations: [
                    ControlFormComponentMock,
                    attrim_form_comp_1.AttrimFormComponent,
                ],
            })
                .compileComponents();
        });
    }
    function initTestSuite() {
        let fixture = testing_1.TestBed.createComponent(attrim_form_comp_1.AttrimFormComponent);
        let gen = new query_data_1.QueryDataGenerator();
        self = {
            compFixture: fixture,
            compDebug: fixture.debugElement,
            comp: fixture.componentInstance,
            dataSource: gen.data(),
        };
        self.comp.queryData = self.dataSource;
        self.compFixture.detectChanges();
    }
    it('selects an option on user click', (done) => __awaiter(this, void 0, void 0, function* () {
        let clsWithOptToSelect = faker.random.arrayElement(self.dataSource.attrimClsArray);
        let optToSelect = faker.random.arrayElement(clsWithOptToSelect.options);
        let optToSelectIsSelectedSource = optToSelect.isSelected;
        let optToChangeSelector = platform_browser_1.By.css(`[name='${clsWithOptToSelect.code}'][value='${optToSelect.value}']`);
        let optToSelectDebug = self.compDebug.query(optToChangeSelector);
        expect(optToSelectDebug).not.toBeNull();
        optToSelectDebug.nativeElement.click();
        yield self.compFixture.whenStable();
        expect(optToSelect.isSelected).not.toBe(optToSelectIsSelectedSource);
        done();
    }));
    let ControlFormComponentMock = class ControlFormComponentMock {
        constructor() {
            let gen = new query_data_1.QueryDataGenerator();
            this.queryData = gen.data();
        }
    };
    ControlFormComponentMock = __decorate([
        core_1.Component({
            selector: 'control-form',
            template: '<attrim-form [queryData]="queryData"></attrim-form>',
        }),
        __metadata("design:paramtypes", [])
    ], ControlFormComponentMock);
});
//# sourceMappingURL=attrim-form.comp.spec.js.map