import {Component} from '@angular/core'
import {Input} from '@angular/core'
import {Output} from '@angular/core'
import {EventEmitter} from '@angular/core'

import {QueryData} from 'app/shared/query-data/query-data.model'
import {Sorting} from 'app/shared/query-data/query-data.model'


@Component({
    selector: 'sorting-form',
    moduleId: module.id,
    templateUrl: 'sorting-form.comp.html',
    styleUrls: ['sorting-form.comp.css'],
})
export class SortingFormComponent {
    sorting = Sorting

    @Input()
    queryData: QueryData

    @Output()
    updatedEvent: EventEmitter<void> = new EventEmitter<void>()

    // noinspection JSUnusedGlobalSymbols
    setSorting(input: HTMLInputElement) {
        let sortingSelectedKey: string = Sorting[input.value]
        let sortingSelected: Sorting = Sorting[sortingSelectedKey]
        this.queryData.sorting = sortingSelected

        this.updatedEvent.emit()
    }
}
