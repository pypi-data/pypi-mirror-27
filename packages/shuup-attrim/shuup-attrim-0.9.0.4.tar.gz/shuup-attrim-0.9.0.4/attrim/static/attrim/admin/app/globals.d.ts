type LangCode = string


type PrimaryKey = number


type Optional<T> = T | null


//noinspection JSUnusedGlobalSymbols
interface Window {
    DJANGO: DjangoProvidedGlobals
}


interface DjangoProvidedGlobals {
    langCodes: Array<LangCode>
    defaultLang: LangCode
    clsPrimaryKey?: Optional<number>
    isEditForm: boolean
}
