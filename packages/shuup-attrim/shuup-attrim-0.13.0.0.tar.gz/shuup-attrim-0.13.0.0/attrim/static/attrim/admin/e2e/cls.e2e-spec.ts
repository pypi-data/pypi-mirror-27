import {browser} from 'protractor'
import {$} from 'protractor'
import {init} from './utils/init'
import {loadClsNewForm} from './utils/navigation'
import {loadClsEditForm} from './utils/navigation'


// TODO waitForAngular
// TODO remove async (its buggy)
describe('cls', () => {
    beforeAll(async (done) => {
        await init()
        done()
    })

    it('edits the class name', async (done) => {
        await loadClsEditForm()

        let clsNameInputEn = $('#cls-name trans-str input[data-lang-code="en"]')
        let clsNameEnOld = await clsNameInputEn.getAttribute('value')
        let clsNameEnNew = 'new english name'
        await clsNameInputEn.clear()
        await clsNameInputEn.sendKeys(clsNameEnNew)
        await $('#cls-save-button').click()
        await browser.waitForAngular()

        await loadClsEditForm()

        let clsNameInputEnUpdated = $('#cls-name trans-str input[data-lang-code="en"]')
        expect(await clsNameInputEnUpdated.getAttribute('value')).toBe(clsNameEnNew)
        // reset to the old name for the other tests
        await clsNameInputEn.clear()
        await clsNameInputEn.sendKeys(clsNameEnOld)
        await $('#cls-save-button').click()
        await browser.waitForAngular()
        done()
    })

    it('creates a cls', async () => {
        await loadClsNewForm()

        let clsCode = 'cls_code'

        await $('#cls-code input').sendKeys(clsCode)
        await $('#cls-name trans-str input[data-lang-code="en"]').sendKeys('en name')

        await browser.waitForAngularEnabled(false)
        await $('#cls-create-button').click()
        await browser.waitForAngular()
        // protractor 5.1.2 throws an error on the direct location set, for now
        // it seems like that crutch is the only option (I've got the solution
        // somewhere on stackoverflow)
        await browser.sleep(200)
        await browser.wait(async () => await $('cls-form').isPresent())
        await browser.waitForAngularEnabled(true)
        await browser.waitForAngular()

        let clsCodeInputValue = await $('#cls-code input').getAttribute('value')
        expect(clsCodeInputValue).toBe(clsCode)
    })
})
