import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import { Heart, Stethoscope, Bone, Baby, Sparkles, Brain, Eye, Syringe, Award, GraduationCap } from "lucide-react"
import { SiteHeader } from "@/components/site-header"
import { SiteFooter } from "@/components/site-footer"

const services = [
  {
    icon: Stethoscope,
    title: "General Medicine",
    description:
      "Comprehensive primary care services for routine check-ups, preventive care, and treatment of common illnesses.",
    gradient: "from-blue-500/10 to-cyan-500/10",
    iconBg: "bg-gradient-to-br from-blue-500 to-cyan-500",
    doctors: [
      {
        name: "Dr. Sarah Johnson",
        specialty: "Internal Medicine",
        experience: "15+ years",
        education: "MD, Johns Hopkins University",
        image: "/professional-female-doctor-wearing-white-coat-smil.jpg",
      },
      {
        name: "Dr. Michael Chen",
        specialty: "Family Medicine",
        experience: "12+ years",
        education: "MD, Stanford Medical School",
        image: "/professional-asian-male-doctor-in-medical-attire-c.jpg",
      },
    ],
  },
  {
    icon: Heart,
    title: "Cardiology",
    description: "Expert heart care including diagnostics, treatment, and management of cardiovascular conditions.",
    gradient: "from-red-500/10 to-pink-500/10",
    iconBg: "bg-gradient-to-br from-red-500 to-pink-500",
    doctors: [
      {
        name: "Dr. Robert Martinez",
        specialty: "Interventional Cardiology",
        experience: "18+ years",
        education: "MD, Harvard Medical School",
        image: "/experienced-male-cardiologist-doctor-professional-.jpg",
      },
      {
        name: "Dr. Emily Thompson",
        specialty: "Cardiac Surgery",
        experience: "14+ years",
        education: "MD, Yale School of Medicine",
        image: "/professional-female-surgeon-doctor-confident-expre.jpg",
      },
    ],
  },
  {
    icon: Bone,
    title: "Orthopedics",
    description: "Specialized care for bones, joints, ligaments, tendons, and muscles with advanced treatment options.",
    gradient: "from-orange-500/10 to-amber-500/10",
    iconBg: "bg-gradient-to-br from-orange-500 to-amber-500",
    doctors: [
      {
        name: "Dr. James Wilson",
        specialty: "Orthopedic Surgery",
        experience: "20+ years",
        education: "MD, Mayo Clinic",
        image: "/experienced-male-orthopedic-surgeon-professional-p.jpg",
      },
      {
        name: "Dr. Lisa Anderson",
        specialty: "Sports Medicine",
        experience: "10+ years",
        education: "MD, Duke University",
        image: "/female-sports-medicine-doctor-athletic-professiona.jpg",
      },
    ],
  },
  {
    icon: Baby,
    title: "Pediatrics",
    description: "Dedicated healthcare for infants, children, and adolescents with compassionate family-centered care.",
    gradient: "from-pink-500/10 to-rose-500/10",
    iconBg: "bg-gradient-to-br from-pink-500 to-rose-500",
    doctors: [
      {
        name: "Dr. Amanda White",
        specialty: "Pediatric Medicine",
        experience: "13+ years",
        education: "MD, Children's Hospital Boston",
        image: "/friendly-female-pediatrician-doctor-warm-smile-car.jpg",
      },
      {
        name: "Dr. David Lee",
        specialty: "Neonatology",
        experience: "16+ years",
        education: "MD, UCLA Medical Center",
        image: "/asian-male-pediatrician-doctor-gentle-professional.jpg",
      },
    ],
  },
  {
    icon: Sparkles,
    title: "Dermatology",
    description: "Complete skin, hair, and nail care including medical dermatology and cosmetic procedures.",
    gradient: "from-purple-500/10 to-fuchsia-500/10",
    iconBg: "bg-gradient-to-br from-purple-500 to-fuchsia-500",
    doctors: [
      {
        name: "Dr. Jessica Brown",
        specialty: "Cosmetic Dermatology",
        experience: "11+ years",
        education: "MD, Columbia University",
        image: "/professional-female-dermatologist-doctor-elegant-p.jpg",
      },
    ],
  },
  {
    icon: Brain,
    title: "Neurology",
    description: "Advanced treatment for nervous system disorders including brain, spine, and nerve conditions.",
    gradient: "from-indigo-500/10 to-blue-500/10",
    iconBg: "bg-gradient-to-br from-indigo-500 to-blue-500",
    doctors: [
      {
        name: "Dr. Thomas Garcia",
        specialty: "Neurosurgery",
        experience: "22+ years",
        education: "MD, Johns Hopkins",
        image: "/experienced-male-neurosurgeon-doctor-distinguished.jpg",
      },
      {
        name: "Dr. Rachel Kim",
        specialty: "Neurologist",
        experience: "9+ years",
        education: "MD, Northwestern University",
        image: "/asian-female-neurologist-doctor-professional-intel.jpg",
      },
    ],
  },
  {
    icon: Eye,
    title: "Ophthalmology",
    description: "Comprehensive eye care services from routine exams to advanced surgical procedures.",
    gradient: "from-teal-500/10 to-emerald-500/10",
    iconBg: "bg-gradient-to-br from-teal-500 to-emerald-500",
    doctors: [
      {
        name: "Dr. Christopher Davis",
        specialty: "Ophthalmologist",
        experience: "17+ years",
        education: "MD, University of Michigan",
        image: "/male-eye-doctor-ophthalmologist-professional-portr.jpg",
      },
    ],
  },
  {
    icon: Syringe,
    title: "Internal Medicine",
    description: "Expert diagnosis and treatment of adult diseases with focus on prevention and wellness.",
    gradient: "from-cyan-500/10 to-sky-500/10",
    iconBg: "bg-gradient-to-br from-cyan-500 to-sky-500",
    doctors: [
      {
        name: "Dr. Patricia Moore",
        specialty: "Internal Medicine",
        experience: "19+ years",
        education: "MD, University of Pennsylvania",
        image: "/professional-female-internal-medicine-doctor-matur.jpg",
      },
      {
        name: "Dr. Kevin Taylor",
        specialty: "Critical Care Medicine",
        experience: "14+ years",
        education: "MD, Washington University",
        image: "/male-intensive-care-doctor-professional-serious-de.jpg",
      },
    ],
  },
]

export default function ServicesPage() {
  return (
    <div className="min-h-screen">
      <SiteHeader />

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-6 bg-gradient-to-br from-sky-50 via-blue-50 to-cyan-50 overflow-hidden">
        {/* Decorative gradient orbs */}
        <div className="absolute top-20 right-10 w-72 h-72 bg-blue-200/30 rounded-full blur-3xl" />
        <div className="absolute bottom-10 left-10 w-96 h-96 bg-cyan-200/20 rounded-full blur-3xl" />

        <div className="container mx-auto max-w-5xl text-center relative z-10">
          <div className="inline-block px-4 py-2 mb-6 rounded-full bg-primary/10 text-primary text-sm font-semibold">
            Expert Medical Services
          </div>
          <h1 className="text-6xl md:text-7xl font-bold mb-6 text-balance bg-gradient-to-r from-slate-900 via-blue-900 to-slate-900 bg-clip-text text-transparent">
            Our Medical Services
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-pretty leading-relaxed">
            Comprehensive healthcare services delivered by experienced professionals across multiple specialties
          </p>
        </div>
      </section>

      {/* Services Grid with Doctors */}
      <section className="py-20 px-6 bg-white relative">
        <div className="container mx-auto max-w-7xl">
          <div className="space-y-16">
            {services.map((service, index) => {
              const Icon = service.icon
              return (
                <div
                  key={service.title}
                  className="group"
                  style={{
                    animation: `fadeInUp 0.6s ease-out ${index * 0.1}s both`,
                  }}
                >
                  {/* Service Header */}
                  <Card className="p-8 hover:shadow-2xl transition-all duration-300 border-2 hover:border-primary/20 relative overflow-hidden mb-6">
                    <div
                      className={`absolute inset-0 bg-gradient-to-br ${service.gradient} opacity-50 group-hover:opacity-100 transition-opacity duration-300`}
                    />

                    <div className="relative z-10">
                      <div className="flex items-start gap-6">
                        <div
                          className={`w-16 h-16 rounded-2xl ${service.iconBg} flex items-center justify-center group-hover:scale-110 transition-transform duration-300 shadow-lg flex-shrink-0`}
                        >
                          <Icon className="w-8 h-8 text-white" />
                        </div>
                        <div className="flex-1">
                          <h3 className="text-3xl font-bold mb-3 group-hover:text-primary transition-colors">
                            {service.title}
                          </h3>
                          <p className="text-muted-foreground leading-relaxed text-lg">{service.description}</p>
                        </div>
                      </div>
                    </div>
                  </Card>

                  {/* Doctors List */}
                  <div className="grid md:grid-cols-2 gap-6 ml-6">
                    {service.doctors.map((doctor) => (
                      <Card
                        key={doctor.name}
                        className="p-6 hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border-2 hover:border-primary/20"
                      >
                        <div className="flex gap-6">
                          <Avatar className="w-24 h-24 border-4 border-primary/20 shadow-lg flex-shrink-0">
                            <AvatarImage src={doctor.image || "/placeholder.svg"} alt={doctor.name} />
                            <AvatarFallback className="bg-gradient-to-br from-blue-500 to-cyan-500 text-white text-xl font-bold">
                              {doctor.name
                                .split(" ")
                                .map((n) => n[0])
                                .join("")}
                            </AvatarFallback>
                          </Avatar>
                          <div className="flex-1">
                            <h4 className="text-xl font-bold mb-1">{doctor.name}</h4>
                            <p className="text-primary font-semibold mb-3">{doctor.specialty}</p>
                            <div className="space-y-2">
                              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                                <Award className="w-4 h-4 text-primary" />
                                <span>{doctor.experience} experience</span>
                              </div>
                              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                                <GraduationCap className="w-4 h-4 text-primary" />
                                <span>{doctor.education}</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </Card>
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-24 px-6 bg-gradient-to-br from-blue-600 via-cyan-600 to-blue-700 text-white overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-cyan-300/10 rounded-full blur-3xl" />

        <div className="container mx-auto max-w-4xl text-center relative z-10">
          <h2 className="text-5xl font-bold mb-6 text-balance">Need Medical Assistance?</h2>
          <p className="text-xl mb-10 opacity-90 max-w-2xl mx-auto leading-relaxed">
            Book an appointment with our specialists and get the care you deserve
          </p>
          <Button
            size="lg"
            variant="secondary"
            className="h-14 px-8 text-lg font-semibold shadow-xl hover:shadow-2xl hover:scale-105 transition-all"
            asChild
          >
            <Link href="/book">Book Appointment Now</Link>
          </Button>
        </div>
      </section>

      <SiteFooter />
    </div>
  )
}
