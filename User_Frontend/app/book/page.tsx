"use client"
import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Heart, CheckCircle2, MessageSquare, ChevronLeft, ChevronRight, Check } from "lucide-react"
import { cn } from "@/lib/utils"
import { SiteHeader } from "@/components/site-header"

const services = [
  {
    id: "general",
    name: "General Check-up",
    description: "Routine examination of health and general wellness",
  },
  {
    id: "cardiology",
    name: "Cardiology Consultation",
    description: "Heart health assessment and cardiac care",
  },
  {
    id: "orthopedics",
    name: "Orthopedic Treatment",
    description: "Bone, joint, and muscle care",
  },
  {
    id: "pediatrics",
    name: "Pediatric Care",
    description: "Specialized care for children and infants",
  },
  {
    id: "dermatology",
    name: "Dermatology",
    description: "Skin care and dermatological treatments",
  },
  {
    id: "neurology",
    name: "Neurology",
    description: "Brain and nervous system care",
  },
]

const timeSlots = [
  "9:00 AM",
  "9:30 AM",
  "10:00 AM",
  "11:00 AM",
  "11:30 AM",
  "1:00 PM",
  "1:30 PM",
  "2:30 PM",
  "3:30 PM",
  "5:00 PM",
]

const getDaysInMonth = (month: number, year: number) => {
  return new Date(year, month + 1, 0).getDate()
}

const getFirstDayOfMonth = (month: number, year: number) => {
  return new Date(year, month, 1).getDay()
}

const monthNames = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
]

export default function BookAppointmentPage() {
  const [currentStep, setCurrentStep] = useState(1)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [selectedService, setSelectedService] = useState("")
  const [selectedDate, setSelectedDate] = useState<Date | null>(null)
  const [selectedTime, setSelectedTime] = useState("")
  const [currentMonth, setCurrentMonth] = useState(new Date().getMonth())
  const [currentYear, setCurrentYear] = useState(new Date().getFullYear())
  const [patientInfo, setPatientInfo] = useState({
    fullName: "",
    phone: "",
    email: "",
  })
  const [bookingToken, setBookingToken] = useState<string | null>(null)

  const handleNextStep = () => {
    if (currentStep < 4) setCurrentStep(currentStep + 1)
  }

  const handlePrevStep = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1)
  }

  const handleSubmit = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/appointments", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          patient_name: patientInfo.fullName,
          phone: patientInfo.phone,
          service: services.find((s) => s.id === selectedService)?.name || selectedService,
          doctor: "Any Available Doctor", // Placeholder as doctor selection isn't in UI yet
          appointment_datetime: selectedDate ? new Date(selectedDate.setHours(parseInt(selectedTime), 0, 0, 0)).toISOString() : new Date().toISOString(),
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setBookingToken(data.token) // e.g. HSP-12345
        setIsSubmitted(true)
      } else {
        console.error("Booking failed")
        // Handle error (optional: show toast)
      }
    } catch (error) {
      console.error("Error submitting booking:", error)
    }
  }

  const canProceedToNextStep = () => {
    if (currentStep === 1) return selectedService !== ""
    if (currentStep === 2) return selectedDate !== null && selectedTime !== ""
    if (currentStep === 3) return patientInfo.fullName && patientInfo.phone && patientInfo.email
    return false
  }

  const renderCalendar = (monthOffset: number) => {
    const month = (currentMonth + monthOffset) % 12
    const year = currentYear + Math.floor((currentMonth + monthOffset) / 12)
    const daysInMonth = getDaysInMonth(month, year)
    const firstDay = getFirstDayOfMonth(month, year)
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    const days = []
    const weekDays = ["S", "M", "T", "W", "T", "F", "S"]

    // Week day headers
    const headers = weekDays.map((day, i) => (
      <div key={`header-${i}`} className="text-center text-xs font-medium text-muted-foreground py-2">
        {day}
      </div>
    ))

    // Empty cells for days before month starts
    for (let i = 0; i < firstDay; i++) {
      days.push(<div key={`empty-${i}`} className="p-2" />)
    }

    // Days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(year, month, day)
      date.setHours(0, 0, 0, 0)
      const isPast = date < today
      const isSelected =
        selectedDate &&
        selectedDate.getDate() === day &&
        selectedDate.getMonth() === month &&
        selectedDate.getFullYear() === year
      const isToday = date.getTime() === today.getTime()

      days.push(
        <button
          key={`day-${day}`}
          type="button"
          disabled={isPast}
          onClick={() => setSelectedDate(date)}
          className={cn(
            "aspect-square rounded-full text-sm font-medium transition-all",
            "hover:bg-primary/10 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent",
            isSelected && "bg-primary text-primary-foreground hover:bg-primary",
            isToday && !isSelected && "border-2 border-primary",
          )}
        >
          {day}
        </button>,
      )
    }

    return (
      <div className="flex-1">
        <div className="text-center font-semibold text-sm mb-3">
          {monthNames[month]} {year}
        </div>
        <div className="grid grid-cols-7 gap-1">
          {headers}
          {days}
        </div>
      </div>
    )
  }

  if (isSubmitted) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4 bg-gradient-to-br from-blue-50 via-cyan-50 to-teal-50">
        <Card className="max-w-md w-full p-8 text-center shadow-2xl border-0 bg-white">
          <div className="flex justify-center mb-6">
            <div className="w-20 h-20 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center shadow-lg">
              <CheckCircle2 className="w-12 h-12 text-white" />
            </div>
          </div>
          <h2 className="text-3xl font-bold mb-4 bg-gradient-to-r from-blue-600 via-cyan-500 to-teal-400 bg-clip-text text-transparent">
            Appointment Confirmed!
          </h2>
          <p className="text-muted-foreground mb-6 leading-relaxed">
            Your appointment is confirmed. You will receive the receipt and further assistance through our chatbot.
          </p>
          <div className="space-y-3">
            <Button className="w-full" size="lg" asChild>
              <Link href={`https://t.me/TheMedixBot?start=token_${bookingToken || ""}`} target="_blank">
                <MessageSquare className="w-5 h-5 mr-2" />
                Continue on Chatbot (Token: {bookingToken})
              </Link>
            </Button>
            <Button variant="outline" className="w-full bg-transparent" asChild>
              <Link href="/">Return to Home</Link>
            </Button>
          </div>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      <SiteHeader />

      <section className="pt-32 pb-20 px-4 bg-gradient-to-br from-blue-50 via-cyan-50 to-teal-50 min-h-screen">
        <div className="container mx-auto max-w-5xl">
          {/* Progress Steps */}
          <div className="mb-12">
            <div className="flex items-center justify-center gap-2 mb-4">
              {[1, 2, 3, 4].map((step) => (
                <div key={step} className="flex items-center">
                  <div
                    className={cn(
                      "w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all",
                      currentStep >= step ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground",
                    )}
                  >
                    {currentStep > step ? <Check className="w-5 h-5" /> : step}
                  </div>
                  {step < 4 && (
                    <div
                      className={cn("w-16 h-1 mx-2 transition-all", currentStep > step ? "bg-primary" : "bg-muted")}
                    />
                  )}
                </div>
              ))}
            </div>
            <div className="flex items-center justify-center gap-16 text-sm font-medium">
              <span className={cn(currentStep >= 1 ? "text-primary" : "text-muted-foreground")}>Select Service</span>
              <span className={cn(currentStep >= 2 ? "text-primary" : "text-muted-foreground")}>Date & Time</span>
              <span className={cn(currentStep >= 3 ? "text-primary" : "text-muted-foreground")}>Your Details</span>
              <span className={cn(currentStep >= 4 ? "text-primary" : "text-muted-foreground")}>Confirmation</span>
            </div>
          </div>

          {/* Step Content */}
          <Card className="p-8 shadow-2xl border-0 bg-white/95 backdrop-blur">
            {/* Step 1: Select Service */}
            {currentStep === 1 && (
              <div className="space-y-6">
                <div className="text-center mb-8">
                  <h2 className="text-3xl font-bold mb-2">Select a Service</h2>
                  <p className="text-muted-foreground">Choose the medical service you need</p>
                </div>
                <div className="grid md:grid-cols-2 gap-4">
                  {services.map((service) => (
                    <button
                      key={service.id}
                      type="button"
                      onClick={() => setSelectedService(service.id)}
                      className={cn(
                        "p-6 rounded-xl border-2 text-left transition-all hover:shadow-lg",
                        selectedService === service.id
                          ? "border-primary bg-primary/5 shadow-lg"
                          : "border-border hover:border-primary/50",
                      )}
                    >
                      <div className="flex items-start gap-4">
                        <div
                          className={cn(
                            "w-12 h-12 rounded-full flex items-center justify-center shrink-0",
                            selectedService === service.id ? "bg-primary" : "bg-muted",
                          )}
                        >
                          <Heart
                            className={cn(
                              "w-6 h-6",
                              selectedService === service.id ? "text-primary-foreground" : "text-muted-foreground",
                            )}
                          />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h3 className="font-semibold mb-1">{service.name}</h3>
                          <p className="text-sm text-muted-foreground">{service.description}</p>
                        </div>
                        {selectedService === service.id && <CheckCircle2 className="w-6 h-6 text-primary shrink-0" />}
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Step 2: Date & Time */}
            {currentStep === 2 && (
              <div className="space-y-6">
                <div className="text-center mb-8">
                  <h2 className="text-3xl font-bold mb-2">Select Date & Time</h2>
                  <p className="text-muted-foreground">Choose your preferred appointment slot</p>
                </div>

                {/* Dual Calendar */}
                <div className="mb-8">
                  <div className="flex items-center justify-between mb-6">
                    <Button
                      type="button"
                      variant="outline"
                      size="icon"
                      onClick={() => {
                        if (currentMonth === 0) {
                          setCurrentMonth(11)
                          setCurrentYear(currentYear - 1)
                        } else {
                          setCurrentMonth(currentMonth - 1)
                        }
                      }}
                      disabled={currentMonth === new Date().getMonth() && currentYear === new Date().getFullYear()}
                    >
                      <ChevronLeft className="w-4 h-4" />
                    </Button>
                    <div className="text-lg font-semibold">Select Date</div>
                    <Button
                      type="button"
                      variant="outline"
                      size="icon"
                      onClick={() => {
                        if (currentMonth === 11) {
                          setCurrentMonth(0)
                          setCurrentYear(currentYear + 1)
                        } else {
                          setCurrentMonth(currentMonth + 1)
                        }
                      }}
                    >
                      <ChevronRight className="w-4 h-4" />
                    </Button>
                  </div>
                  <div className="flex gap-8 justify-center">
                    {renderCalendar(0)}
                    <div className="hidden lg:block">{renderCalendar(1)}</div>
                  </div>
                </div>

                {/* Time Slots */}
                {selectedDate && (
                  <div>
                    <h3 className="font-semibold mb-4 text-center">Available Times</h3>
                    <div className="flex flex-wrap gap-3 justify-center">
                      {timeSlots.map((time) => (
                        <button
                          key={time}
                          type="button"
                          onClick={() => setSelectedTime(time)}
                          className={cn(
                            "px-6 py-3 rounded-lg font-medium transition-all",
                            selectedTime === time
                              ? "bg-primary text-primary-foreground shadow-lg"
                              : "bg-muted hover:bg-muted/80",
                          )}
                        >
                          {time}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Step 3: Patient Details */}
            {currentStep === 3 && (
              <div className="space-y-6 max-w-xl mx-auto">
                <div className="text-center mb-8">
                  <h2 className="text-3xl font-bold mb-2">Your Details</h2>
                  <p className="text-muted-foreground">Please provide your contact information</p>
                </div>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="fullName">Full Name *</Label>
                    <Input
                      id="fullName"
                      type="text"
                      placeholder="John Doe"
                      value={patientInfo.fullName}
                      onChange={(e) => setPatientInfo({ ...patientInfo, fullName: e.target.value })}
                      className="h-12"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="phone">Phone Number *</Label>
                    <Input
                      id="phone"
                      type="tel"
                      placeholder="(555) 123-4567"
                      value={patientInfo.phone}
                      onChange={(e) => setPatientInfo({ ...patientInfo, phone: e.target.value })}
                      className="h-12"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email">Email Address *</Label>
                    <Input
                      id="email"
                      type="email"
                      placeholder="john@example.com"
                      value={patientInfo.email}
                      onChange={(e) => setPatientInfo({ ...patientInfo, email: e.target.value })}
                      className="h-12"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Step 4: Confirmation */}
            {currentStep === 4 && (
              <div className="space-y-6 max-w-xl mx-auto">
                <div className="text-center mb-8">
                  <h2 className="text-3xl font-bold mb-2">Review & Confirm</h2>
                  <p className="text-muted-foreground">Please review your appointment details</p>
                </div>
                <div className="space-y-4 bg-muted/50 rounded-xl p-6">
                  <div className="flex justify-between items-center py-3 border-b">
                    <span className="text-muted-foreground">Service</span>
                    <span className="font-semibold">{services.find((s) => s.id === selectedService)?.name}</span>
                  </div>
                  <div className="flex justify-between items-center py-3 border-b">
                    <span className="text-muted-foreground">Date</span>
                    <span className="font-semibold">{selectedDate?.toLocaleDateString()}</span>
                  </div>
                  <div className="flex justify-between items-center py-3 border-b">
                    <span className="text-muted-foreground">Time</span>
                    <span className="font-semibold">{selectedTime}</span>
                  </div>
                  <div className="flex justify-between items-center py-3 border-b">
                    <span className="text-muted-foreground">Patient</span>
                    <span className="font-semibold">{patientInfo.fullName}</span>
                  </div>
                  <div className="flex justify-between items-center py-3 border-b">
                    <span className="text-muted-foreground">Phone</span>
                    <span className="font-semibold">{patientInfo.phone}</span>
                  </div>
                  <div className="flex justify-between items-center py-3">
                    <span className="text-muted-foreground">Email</span>
                    <span className="font-semibold">{patientInfo.email}</span>
                  </div>
                </div>
              </div>
            )}

            {/* Navigation Buttons */}
            <div className="flex items-center justify-between mt-8 pt-6 border-t">
              <Button
                type="button"
                variant="outline"
                onClick={handlePrevStep}
                disabled={currentStep === 1}
                className="px-8 bg-transparent"
              >
                <ChevronLeft className="w-4 h-4 mr-2" />
                Previous
              </Button>
              {currentStep < 4 ? (
                <Button type="button" onClick={handleNextStep} disabled={!canProceedToNextStep()} className="px-8">
                  Next
                  <ChevronRight className="w-4 h-4 ml-2" />
                </Button>
              ) : (
                <Button type="button" onClick={handleSubmit} className="px-8">
                  Confirm Appointment
                </Button>
              )}
            </div>
          </Card>
        </div>
      </section>
    </div>
  )
}
