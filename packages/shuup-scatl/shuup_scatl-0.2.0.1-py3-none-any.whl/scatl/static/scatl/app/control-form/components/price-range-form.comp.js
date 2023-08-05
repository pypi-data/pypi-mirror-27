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
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = require("@angular/core");
const core_2 = require("@angular/core");
const core_3 = require("@angular/core");
const core_4 = require("@angular/core");
const forms_1 = require("@angular/forms");
const query_data_model_1 = require("app/shared/query-data/query-data.model");
const core_5 = require("@angular/core");
let PriceRangeFormComponent = class PriceRangeFormComponent {
    constructor(formBuilder) {
        this.updatedEvent = new core_4.EventEmitter();
        this.config = {
            connect: true,
            step: 1,
            range: {
                min: window.DJANGO.priceRange.min,
                max: window.DJANGO.priceRange.max,
            },
            tooltips: [false, false],
        };
        // TODO initial data from queryData, because can be different if loaded from the url
        this.priceRange = [
            window.DJANGO.priceRange.min,
            window.DJANGO.priceRange.max,
        ];
        this.formBuilder = formBuilder;
    }
    ngOnInit() {
        this.formGroup = this.formBuilder.group({
            slider: [this.priceRange],
            priceMin: [this.priceRange[0]],
            priceMax: [this.priceRange[1]],
        });
    }
    // noinspection JSUnusedGlobalSymbols
    updateFromMinInput(value) {
        this.queryData.priceRange.min = Number(value);
        this.syncPriceRangeForm();
        this.updatedEvent.emit();
    }
    // noinspection JSUnusedGlobalSymbols
    updateFromMaxInput(value) {
        this.queryData.priceRange.max = Number(value);
        this.syncPriceRangeForm();
        this.updatedEvent.emit();
    }
    // noinspection JSUnusedGlobalSymbols
    updateFromSlider() {
        this.queryData.priceRange.min = this.priceRange[0];
        this.queryData.priceRange.max = this.priceRange[1];
        this.syncPriceRangeForm();
        this.updatedEvent.emit();
    }
    /**
     * ngModel won't help, because of the angular bug with the input[type=number]
     */
    syncPriceRangeForm() {
        let formControls = this.formGroup.controls;
        let slider = formControls['slider'];
        slider.setValue([this.queryData.priceRange.min, this.queryData.priceRange.max]);
        let priceMin = formControls['priceMin'];
        priceMin.setValue(this.queryData.priceRange.min);
        let priceMax = formControls['priceMax'];
        priceMax.setValue(this.queryData.priceRange.max);
    }
};
__decorate([
    core_2.Input(),
    __metadata("design:type", query_data_model_1.QueryData)
], PriceRangeFormComponent.prototype, "queryData", void 0);
__decorate([
    core_3.Output(),
    __metadata("design:type", core_4.EventEmitter)
], PriceRangeFormComponent.prototype, "updatedEvent", void 0);
PriceRangeFormComponent = __decorate([
    core_1.Component({
        selector: 'price-range-form',
        moduleId: module.id,
        templateUrl: 'price-range-form.comp.html',
        styleUrls: ['price-range-form.comp.css'],
        encapsulation: core_5.ViewEncapsulation.None,
    }),
    __metadata("design:paramtypes", [forms_1.FormBuilder])
], PriceRangeFormComponent);
exports.PriceRangeFormComponent = PriceRangeFormComponent;
//# sourceMappingURL=price-range-form.comp.js.map