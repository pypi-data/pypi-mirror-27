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
const platform_browser_2 = require("@angular/platform-browser");
const forms_1 = require("@angular/forms");
const forms_2 = require("@angular/forms");
const ng2_nouislider_1 = require("ng2-nouislider");
const ng2_nouislider_2 = require("ng2-nouislider");
const price_range_form_comp_1 = require("app/control-form/components/price-range-form.comp");
const core_1 = require("@angular/core");
const django_env_1 = require("testutils/mocks/django-env");
describe('price-range', () => {
    let self;
    beforeEach((done) => __awaiter(this, void 0, void 0, function* () {
        django_env_1.initDjangoEnv();
        yield initAngularEnv();
        initTestSuite();
        done();
    }));
    function initAngularEnv() {
        return __awaiter(this, void 0, void 0, function* () {
            yield testing_1.TestBed.configureTestingModule({
                imports: [
                    platform_browser_2.BrowserModule,
                    forms_1.FormsModule,
                    forms_2.ReactiveFormsModule,
                    ng2_nouislider_1.NouisliderModule,
                ],
                declarations: [
                    ControlFormComponentMock,
                    price_range_form_comp_1.PriceRangeFormComponent,
                ],
            })
                .compileComponents();
        });
    }
    function initTestSuite() {
        let fixture = testing_1.TestBed.createComponent(price_range_form_comp_1.PriceRangeFormComponent);
        self = {
            compFixture: fixture,
            compDebug: fixture.debugElement,
            comp: fixture.componentInstance,
        };
        let gen = new query_data_1.QueryDataGenerator();
        self.comp.queryData = gen.data();
        self.compFixture.detectChanges();
    }
    it('changes the `min` priceRange input', () => {
        testPriceRangeUpdate('min');
    });
    it('changes the `max` priceRange input', () => {
        testPriceRangeUpdate('max');
    });
    it('syncs the price range inputs with the slider', () => {
        let sliderDebug = self.compDebug.query(platform_browser_1.By.directive(ng2_nouislider_2.NouisliderComponent));
        let sliderInstance = sliderDebug.componentInstance;
        let priceRangeMin = 200;
        let priceRangeMax = 15000;
        sliderInstance.slider.set([priceRangeMin, priceRangeMax]);
        self.compFixture.detectChanges();
        let priceRangeMinDebug = self.compDebug.query(platform_browser_1.By.css(`input[name='price-min']`));
        expect(priceRangeMinDebug.properties['value']).toBe(priceRangeMin);
        let priceRangeMaxDebug = self.compDebug.query(platform_browser_1.By.css(`input[name='price-max']`));
        expect(priceRangeMaxDebug.properties['value']).toBe(priceRangeMax);
    });
    it('syncs the price range slider with the inputs', () => {
        let priceRangeMin = 200;
        let priceRangeMax = 15000;
        setInputValue({ name: `price-min`, value: priceRangeMin });
        setInputValue({ name: `price-max`, value: priceRangeMax });
        self.compFixture.detectChanges();
        expect(self.comp.formGroup.value).toEqual({
            slider: [priceRangeMin, priceRangeMax],
            priceMin: priceRangeMin,
            priceMax: priceRangeMax,
        });
    });
    function testPriceRangeUpdate(priceRangeInput) {
        let priceRangeInputValue = 1000;
        setInputValue({
            name: `price-${priceRangeInput}`,
            value: priceRangeInputValue,
        });
        self.compFixture.detectChanges();
        let priceRangeValue = self.comp.queryData.priceRange[priceRangeInput];
        expect(priceRangeValue).toBe(priceRangeInputValue);
    }
    function setInputValue(args) {
        let inputDebug = self.compDebug.query(platform_browser_1.By.css(`input[name='${args.name}']`));
        inputDebug.nativeElement.value = args.value;
        let changeEvent = createEvent('change');
        inputDebug.nativeElement.dispatchEvent(changeEvent);
    }
    function createEvent(eventName) {
        let event = document.createEvent('CustomEvent');
        event.initCustomEvent(eventName, false, false, null);
        return event;
    }
    let ControlFormComponentMock = class ControlFormComponentMock {
    };
    ControlFormComponentMock = __decorate([
        core_1.Component({
            selector: 'control-form',
            template: '<price-range-form [queryData]="queryData"></price-range-form>',
        })
    ], ControlFormComponentMock);
});
//# sourceMappingURL=price-range-form.comp.spec.js.map