import { Job as JobType } from "../Interfaces"

interface JobComponentProps {
    job: JobType;
}

export default function JobComponent({ job }: JobComponentProps) {

    return (
        <>
            <div className="flex flex-col bg-zinc-100 gap-3 p-20">
                <h1 className="text-3xl font-medium">{job.title}</h1>
                <a href={job.url}>Link to job webpage</a>
                <h2 className="text-2xl font-semibold">{job.position}</h2>
                <h3 className="text-2xl font-semibold">{job.location}</h3>
                <div className="mt-5 flex">
                    <div className="w-1/12 bg-amber-900 mr-5"></div>
                    <p className="text-2xl">{job.about}</p>
                </div>
            </div>
        </>
    )
}
