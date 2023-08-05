import {Component} from '@angular/core'
import {Input} from '@angular/core'
import {Output} from '@angular/core'
import {EventEmitter} from '@angular/core'
import {FormGroup} from '@angular/forms'
import {OnInit} from '@angular/core'
import {FormBuilder} from '@angular/forms'
import {FormControl} from '@angular/forms'
import {QueryData} from 'app/shared/query-data/query-data.model'
import {ViewEncapsulation} from '@angular/core'


declare var window: any


@Component({
    selector: 'price-range-form',
    moduleId: module.id,
    templateUrl: 'price-range-form.comp.html',
    styleUrls: ['price-range-form.comp.css'],
    encapsulation: ViewEncapsulation.None,
})
export class PriceRangeFormComponent implements OnInit {
    @Input()
    queryData: QueryData

    @Output()
    updatedEvent: EventEmitter<void> = new EventEmitter<void>()

    formGroup: FormGroup
    config: any = {
        connect: true,
        step: 1,
        range: {
            min: window.DJANGO.priceRange.min,
            max: window.DJANGO.priceRange.max,
        },
        tooltips: [false, false],
    }
    // TODO initial data from queryData, because can be different if loaded from the url
    priceRange: Array<number> = [
        window.DJANGO.priceRange.min,
        window.DJANGO.priceRange.max,
    ]

    private formBuilder: FormBuilder

    constructor(formBuilder: FormBuilder) {
        this.formBuilder = formBuilder
    }

    ngOnInit() {
        this.formGroup = this.formBuilder.group({
            slider: [this.priceRange],
            priceMin: [this.priceRange[0]],
            priceMax: [this.priceRange[1]],
        })
    }

    // noinspection JSUnusedGlobalSymbols
    updateFromMinInput(value: string) {
        this.queryData.priceRange!!.min = Number(value)
        this.syncPriceRangeForm()
        this.updatedEvent.emit()
    }

    // noinspection JSUnusedGlobalSymbols
    updateFromMaxInput(value: string) {
        this.queryData.priceRange!!.max = Number(value)
        this.syncPriceRangeForm()
        this.updatedEvent.emit()
    }

    // noinspection JSUnusedGlobalSymbols
    updateFromSlider() {
        this.queryData.priceRange!!.min = this.priceRange[0]
        this.queryData.priceRange!!.max = this.priceRange[1]
        this.syncPriceRangeForm()
        this.updatedEvent.emit()
    }

    /**
     * ngModel won't help, because of the angular bug with the input[type=number]
     */
    private syncPriceRangeForm() {
        let formControls = this.formGroup.controls

        let slider: FormControl = formControls['slider'] as FormControl
        slider.setValue([this.queryData.priceRange!!.min, this.queryData.priceRange!!.max])

        let priceMin: FormControl = formControls['priceMin'] as FormControl
        priceMin.setValue(this.queryData.priceRange!!.min)

        let priceMax: FormControl = formControls['priceMax'] as FormControl
        priceMax.setValue(this.queryData.priceRange!!.max)
    }
}
