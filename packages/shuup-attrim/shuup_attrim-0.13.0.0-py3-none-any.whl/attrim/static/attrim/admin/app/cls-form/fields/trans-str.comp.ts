import {Component} from '@angular/core'
import {Input} from '@angular/core'
import {Output} from '@angular/core'
import {EventEmitter, OnInit} from '@angular/core'
import {TransStr} from 'app/models/trans-str.model'
import {ViewEncapsulation} from '@angular/core'


@Component({
    selector: 'trans-str',
    moduleId: module.id,
    templateUrl: 'trans-str.comp.html',
    styleUrls: ['trans-str.comp.css'],
    // the encapsulation is screwed up for dynamic components in 4.0.3
    encapsulation: ViewEncapsulation.None,
})
export class TransStrComponent implements OnInit {
    @Input() translations: TransStr
    // must reflect the pattern `{orig_name}Change` for the `[(ngModel)]` binding
    @Output() translationsChange = new EventEmitter<TransStr>()

    // noinspection JSMismatchedCollectionQueryUpdate
    protected langCodes: Array<LangCode> = window.DJANGO.langCodes
    protected langCodeSelected: LangCode = window.DJANGO.defaultLang

    ngOnInit() {
        this.initTranslation()
    }

    // noinspection JSUnusedLocalSymbols
    protected selectLangCode(langCode: LangCode) {
        this.langCodeSelected = langCode
    }

    protected setButtonClasses(langCode: LangCode): {[className: string]: boolean} {
        let isEmpty = this.isTranslationEmpty(langCode)
        if (isEmpty) {
            let unfilledIcon = {square: true, outline: true, icon: true}
            return unfilledIcon
        } else {
            let filledIcon = {checkmark: true, box: true, icon: true}
            return filledIcon
        }
    }

    protected updateTranslations(langCode: LangCode, value: string) {
        this.translations[langCode] = value
        this.translationsChange.emit(this.translations)
    }

    private initTranslation() {
        if (this.translations === undefined) {
            this.translations = {}
        }
        for (let langCode of window.DJANGO.langCodes) {
            this.translations[langCode] = ''
        }
    }

    private isTranslationEmpty(langCode: LangCode): boolean {
        let transCurrent = this.translations[langCode]
        let isEmpty = transCurrent === '' || transCurrent === undefined
        let isNotDefaultTrans = langCode !== window.DJANGO.defaultLang
        let isMirroringDefaultTrans = (
            transCurrent === this.translations[window.DJANGO.defaultLang]
        )
        return isEmpty || (isNotDefaultTrans && isMirroringDefaultTrans)
    }
}
