// TODO move out the notify logic
/** It will break without the semicolons. */
export function asyncNotifyOn(messages: {success?: string, error: string}) {
    return (target: Object, propertyKey: string, descriptor: TypedPropertyDescriptor<any>) => {
        let originalMethod = descriptor.value
        descriptor.value = async function(...args: any[]): Promise<any> {
            let result: any
            try {
                result = await originalMethod.apply(this, args);
                if (messages.success !== undefined) {
                    (this as any).notifyService.success(messages.success);
                }
            } catch (error) {
                (this as any).notifyService.error(messages.error, error);
            }
            return result
        }
        return descriptor
    }
}
