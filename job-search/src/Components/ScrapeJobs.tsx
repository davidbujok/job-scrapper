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
            <div className="flex h-24 mb-16 bg-amber-800 justify-center gap-5">
                <div className="w-1/12 h-4/6 self-center gap-3 flex flex-col">
                </div>
                <div className="w-1/3 h-4/6 self-center gap-3 flex">
                    <div className="self-center">
                        <p className="font-bold text-white">Job</p>
                        <input className="bg-grey-50 w-full py-2 font-medium px-3 leading-tight focus:outline-none focus:shadow-outline"
                            onChange={(e) => setJob(e.target.value)}
                            value={job}
                        />
                    </div>
                </div>
                <div className="w-1/3 h-4/6 self-center gap-3 flex">
                    <div className="self-center">
                        <p className="font-bold text-white">Location</p>
                        <input className="bg-grey-50 w-full py-2 font-medium px-3 focus:outline-none focus:shadow-outline"
                            onChange={(e) => setLocation(e.target.value)}
                            value={location}
                        />
                    </div>
                </div>
                <div className="w-1/3 h-4/6 self-center justify-center gap-3 flex flex-col">
                    <div className="flex justify-between">
                    </div>
                    <button onClick={() => activateScraping(job, location)} className="text-2xl font-semibold text-white">Start</button>
                </div>
                <div className="w-1/3 h-4/6 self-center justify-center gap-3 flex flex-col">
                    <div className="flex justify-between">
                    </div>
                    <button onClick={() => setScrapePage(false)} className="text-2xl font-semibold text-amber-200">Cancel</button>
                </div>
            </div>
        </>
    )

}
