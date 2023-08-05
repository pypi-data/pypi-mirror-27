import {FormsModule} from '@angular/forms'
import {async} from '@angular/core/testing'
import {By} from '@angular/platform-browser'
import {TestBed} from '@angular/core/testing'
import {ComponentFixture} from '@angular/core/testing'

import {TransStrComponent} from 'app/cls-form/fields/trans-str.comp'
import {DebugElement} from '@angular/core'


describe('trans str tests', () => {
    let self: {
        fixture: ComponentFixture<TransStrComponent>
        debugElem: DebugElement
        defaultLang: LangCode,
        langCodes: Array<LangCode>
    }

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            imports: [FormsModule],
            declarations: [TransStrComponent],
        })
        TestBed.compileComponents()
    }))

    beforeEach(() => {
        let fixture = TestBed.createComponent(TransStrComponent)
        self = {
            fixture: fixture,
            debugElem: fixture.debugElement,
            defaultLang: window.DJANGO.defaultLang,
            langCodes: window.DJANGO.langCodes,
        }
        self.fixture.detectChanges()
    })

    it('updates the buttons statuses on input change', () => {
        let root = self.fixture.debugElement
        let input = root.query(By.css('input'))
        input.nativeElement.value = 'new value'
        input.nativeElement.dispatchEvent(new Event('input'))

        self.fixture.detectChanges()

        let filledIconClasses = '.checkmark.box'
        let filledButton = self.debugElem.query(By.css(filledIconClasses))
        expect(filledButton).not.toBeNull()
    })

    it('dynamically displays the active lang code input', async(async () => {
        expect(self.defaultLang).toBe(self.langCodes[0])

        let input0 = await selectLangInputByLangCodeIndex(0)
        let input0ValueNew = 'input 0 value new'
        setInputValue(input0, input0ValueNew)
        expect(input0.nativeElement.value).toBe(input0ValueNew)

        let input1 = await selectLangInputByLangCodeIndex(1)
        expect(input1.nativeElement.value).toBe('')

        input0 = await selectLangInputByLangCodeIndex(0)
        expect(input0.nativeElement.value).toBe(input0ValueNew)

        input1 = await selectLangInputByLangCodeIndex(1)
        expect(input1.nativeElement.value).toBe('')
        let input1ValueNew = 'input 1 value new'
        setInputValue(input1, input1ValueNew)
        expect(input1.nativeElement.value).toBe(input1ValueNew)

        input0 = await selectLangInputByLangCodeIndex(0)
        expect(input0.nativeElement.value).toBe(input0ValueNew)
    }))

    async function selectLangInputByLangCodeIndex(
        langIndex: number,
    ): Promise<DebugElement> {
        let selectLangButton = self.debugElem.query(
            By.css(`.select-lang-button[data-lang-code='${self.langCodes[langIndex]}']`)
        )
        selectLangButton.triggerEventHandler('click', null)
        self.fixture.detectChanges()

        // otherwise it fails to sync the input with respect to the selected
        // lang code
        await self.fixture.whenStable()

        let input = self.debugElem.query(
            By.css(`input[data-lang-code='${self.langCodes[langIndex]}']`)
        )
        return input
    }

    function setInputValue(input: DebugElement, value: string) {
        input.nativeElement.value = value
        input.nativeElement.dispatchEvent(new Event('input'))
    }
})
