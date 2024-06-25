export function titleCleaner(jobTitle: string) {

    const reJob = /(- job.*$)/
    const result = jobTitle.replace(reJob, "")

    return result
}
export function capitalizeFirstLetter(text: string, comma: boolean) {
    const words = text.split(" ")
    let capitalized = ""
    let word_break = " "
    if (comma) {
        word_break = ", "
    }
    for ( let i = 0; i < words.length; i++ ) {
        if (i < words.length - 1) {
            capitalized += words[i][0].toUpperCase() + words[i].slice(1,) + word_break
        } else {
            capitalized += words[i][0].toUpperCase() + words[i].slice(1,)
        }
    }
    return capitalized
}
