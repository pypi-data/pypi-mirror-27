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
const query_data_model_1 = require("app/shared/query-data/query-data.model");
let AttrimFormComponent = class AttrimFormComponent {
    constructor() {
        this.updatedEvent = new core_4.EventEmitter();
    }
    // noinspection JSUnusedGlobalSymbols
    setQueryData(input) {
        let isClsFromInput = (cls) => cls.code === input.name;
        let clsFromInput = this.queryData.attrimClsArray.find(isClsFromInput);
        let isOptionFromInput = (clsOption) => {
            return clsOption.value === input.value;
        };
        let optionFromInput = clsFromInput.options.find(isOptionFromInput);
        optionFromInput.isSelected = input.checked;
        this.updatedEvent.emit();
    }
};
__decorate([
    core_2.Input(),
    __metadata("design:type", query_data_model_1.QueryData)
], AttrimFormComponent.prototype, "queryData", void 0);
__decorate([
    core_3.Output(),
    __metadata("design:type", core_4.EventEmitter)
], AttrimFormComponent.prototype, "updatedEvent", void 0);
AttrimFormComponent = __decorate([
    core_1.Component({
        selector: 'attrim-form',
        moduleId: module.id,
        templateUrl: 'attrim-form.comp.html',
        styleUrls: ['attrim-form.comp.css'],
    })
], AttrimFormComponent);
exports.AttrimFormComponent = AttrimFormComponent;
//# sourceMappingURL=attrim-form.comp.js.map