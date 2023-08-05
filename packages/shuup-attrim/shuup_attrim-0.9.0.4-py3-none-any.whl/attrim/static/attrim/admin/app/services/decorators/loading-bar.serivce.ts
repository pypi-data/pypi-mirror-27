export function asyncShowLoadingBar(
    target: Object,
    propertyKey: string,
    descriptor: TypedPropertyDescriptor<any>,
): TypedPropertyDescriptor<any> {
    let originalMethod = descriptor.value
    descriptor.value = async function(...args: any[]): Promise<any> {
        (this as any).loadingBarService.start();
        let result: any = await originalMethod.apply(this, args);
        (this as any).loadingBarService.complete();
        return result;
    }
    return descriptor
}
