import { Dispatch, useState } from "react"

interface JobProps {
    setScrapePage: Dispatch<React.SetStateAction<boolean>>
}

export default function ScrapeJobs({ setScrapePage }: JobProps) {
    const [job, setJob] = useState<string>("")
    const [location, setLocation] = useState<string>("")

    const activateScraping = async (job: string, location: string) => {
        console.log("Parameters to send:", job, location);
        try {
            const response = await fetch(`http://127.0.0.1:5000/runscript/${job}/${location}`, { method: 'POST' });
            const data = await response.json();
            console.log('Response from server:', data);
        } catch (error) {
            console.error('Error during fetch:', error);
        }
    };


    return (
        <>
            <div className="flex h-48 mb-16 border border-red-300 justify-center gap-5 ml-9 mr-9">
                <div className="w-1/12 h-4/6 self-center gap-3 flex flex-col">
                </div>
                <div className="w-1/3 h-4/6 self-center gap-3 flex flex-col">
                    <p className="text-3xl font-bold">Job</p>
                    <input className="bg-stone-300 w-full py-2 text-3xl font-medium px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        onChange={(e) => setJob(e.target.value)}
                        value={job}
                    />
                    <p>{job}</p>
                </div>
                <div className="w-1/3 h-4/6 self-center gap-3 flex flex-col">
                    <div className="flex justify-between">
                        <p className="text-3xl font-bold">Location</p>
                    </div>
                    <input className="bg-stone-300 w-full py-2 text-3xl font-medium px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        onChange={(e) => setLocation(e.target.value)}
                        value={location}
                    />
                    <p>{location}</p>
                </div>
                <div className="w-1/3 h-4/6 self-center justify-center gap-3 flex flex-col">
                    <div className="flex justify-between">
                    </div>
                    <button onClick={() => activateScraping(job, location)} className="text-4xl font-semibold text-green-600">Start</button>
                </div>
                <div className="w-1/3 h-4/6 self-center justify-center gap-3 flex flex-col">
                    <div className="flex justify-between">
                    </div>
                    <button onClick={() => setScrapePage(false)} className="text-4xl font-semibold text-red-600">Cancel</button>
                </div>
            </div>
        </>
    )

}
