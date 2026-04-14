import { useState, useEffect } from 'react'
import axios from 'axios'
import { PlusCircle, Trash2, CheckCircle, BookOpen } from 'lucide-react'

function App() {
    const [notes, setNotes] = useState([])
    const [title, setTitle] = useState('')
    const [description, setDescription] = useState('')
    const [difficulty, setDifficulty] = useState('Medium')

    const API_URL = 'http://localhost:8000/notes'

    useEffect(() => {
        fetchNotes()
    }, [])

    const fetchNotes = async () => {
        try {
            const response = await axios.get(API_URL)
            setNotes(response.data)
        } catch (error) {
            console.error("Error fetching notes:", error)
        }
    }

    const addNote = async (e) => {
        e.preventDefault()
        if (!title || !description) return

        try {
            await axios.post(API_URL, {
                title,
                concept_description: description,
                difficulty,
                completed: false
            })
            setTitle('')
            setDescription('')
            fetchNotes()
        } catch (error) {
            console.error("Error adding note:", error)
        }
    }

    const toggleComplete = async (id, currentStatus) => {
        try {
            await axios.put(`${API_URL}/${id}`, {
                completed: !currentStatus
            })
            fetchNotes()
        } catch (error) {
            console.error("Error updating note:", error)
        }
    }

    const deleteNote = async (id) => {
        try {
            await axios.delete(`${API_URL}/${id}`)
            fetchNotes()
        } catch (error) {
            console.error("Error deleting note:", error)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black p-8 font-sans">
            <div className="max-w-6xl mx-auto flex flex-col md:flex-row gap-8">

                {/* Left Section: Form */}
                <div className="w-full md:w-1/3 glass p-6 rounded-2xl shadow-xl h-fit border-t border-l border-white/10 relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>

                    <div className="flex items-center gap-3 mb-8">
                        <BookOpen className="text-blue-400 w-8 h-8" />
                        <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">Python Tracker</h1>
                    </div>

                    <form onSubmit={addNote} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-1">Concept Title</label>
                            <input
                                type="text"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                className="w-full bg-black/30 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                                placeholder="e.g., List Comprehensions"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-1">Description / Notes</label>
                            <textarea
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                                className="w-full bg-black/30 border border-gray-600 rounded-lg px-4 py-2 text-white h-32 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all resize-none"
                                placeholder="Write your explanation here..."
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-1">Difficulty</label>
                            <select
                                value={difficulty}
                                onChange={(e) => setDifficulty(e.target.value)}
                                className="w-full bg-black/30 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all appearance-none"
                            >
                                <option value="Easy" className="bg-gray-800">Easy</option>
                                <option value="Medium" className="bg-gray-800">Medium</option>
                                <option value="Hard" className="bg-gray-800">Hard</option>
                            </select>
                        </div>

                        <button
                            type="submit"
                            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-semibold py-3 rounded-lg flex items-center justify-center gap-2 transition-all transform hover:scale-[1.02] active:scale-95 shadow-lg shadow-blue-500/20"
                        >
                            <PlusCircle size={20} />
                            Save Concept
                        </button>
                    </form>
                </div>

                {/* Right Section: Notes Grid */}
                <div className="w-full md:w-2/3">
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-xl font-semibold text-gray-200">Your Learning Journey</h2>
                        <span className="bg-gray-800 text-blue-400 px-3 py-1 rounded-full text-sm font-medium border border-gray-700">
                            {notes.length} {notes.length === 1 ? 'Concept' : 'Concepts'}
                        </span>
                    </div>

                    {notes.length === 0 ? (
                        <div className="glass h-64 rounded-2xl flex flex-col items-center justify-center text-gray-400 border border-dashed border-gray-600">
                            <BookOpen size={48} className="mb-4 opacity-50" />
                            <p>Nothing tracked yet.</p>
                            <p className="text-sm">Add your first Python concept to get started!</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            {notes.map((note) => (
                                <div
                                    key={note.id}
                                    className={`glass p-5 rounded-xl border-l-4 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-xl ${note.completed ? 'border-l-green-500 opacity-70' : 'border-l-blue-500'
                                        }`}
                                >
                                    <div className="flex justify-between items-start mb-2">
                                        <h3 className={`text-lg font-semibold ${note.completed ? 'line-through text-gray-400' : 'text-white'}`}>
                                            {note.title}
                                        </h3>
                                        <span className={`text-xs px-2 py-1 rounded shadow-sm ${note.difficulty === 'Easy' ? 'bg-green-500/20 text-green-300' :
                                                note.difficulty === 'Medium' ? 'bg-yellow-500/20 text-yellow-300' :
                                                    'bg-red-500/20 text-red-300'
                                            }`}>
                                            {note.difficulty}
                                        </span>
                                    </div>

                                    <p className={`text-sm mb-4 line-clamp-3 ${note.completed ? 'text-gray-500' : 'text-gray-300'}`}>
                                        {note.concept_description}
                                    </p>

                                    <div className="flex justify-between items-center pt-2 border-t border-gray-700/50">
                                        <button
                                            onClick={() => toggleComplete(note.id, note.completed)}
                                            className={`flex items-center gap-1 text-sm font-medium transition-colors ${note.completed ? 'text-green-400 hover:text-green-300' : 'text-gray-400 hover:text-white'
                                                }`}
                                        >
                                            <CheckCircle size={16} />
                                            {note.completed ? 'Learned' : 'Mark Learned'}
                                        </button>

                                        <button
                                            onClick={() => deleteNote(note.id)}
                                            className="text-red-400 hover:text-red-300 transition-colors p-1 rounded hover:bg-red-400/10"
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default App
