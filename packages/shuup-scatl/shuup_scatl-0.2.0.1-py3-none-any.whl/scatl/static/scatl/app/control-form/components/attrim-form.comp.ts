import {Component} from '@angular/core'
import {Input} from '@angular/core'
import {Output} from '@angular/core'
import {EventEmitter} from '@angular/core'

import {QueryData} from 'app/shared/query-data/query-data.model'
import {AttrimCls} from 'app/shared/query-data/query-data.model'
import {AttrimOption} from 'app/shared/query-data/query-data.model'


@Component({
    selector: 'attrim-form',
    moduleId: module.id,
    templateUrl: 'attrim-form.comp.html',
    styleUrls: ['attrim-form.comp.css'],
})
export class AttrimFormComponent {
    @Input()
    queryData: QueryData

    @Output()
    updatedEvent: EventEmitter<void> = new EventEmitter<void>()

    // noinspection JSUnusedGlobalSymbols
    setQueryData(input: HTMLInputElement) {
        let isClsFromInput = (cls: AttrimCls): boolean => cls.code === input.name
        let clsFromInput = this.queryData.attrimClsArray.find(isClsFromInput)!!
        let isOptionFromInput = (clsOption: AttrimOption): boolean => {
            return clsOption.value === input.value
        }
        let optionFromInput = clsFromInput.options.find(isOptionFromInput)!!
        optionFromInput.isSelected = input.checked

        this.updatedEvent.emit()
    }
}
